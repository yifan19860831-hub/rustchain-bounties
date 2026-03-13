/*
 * RUSTCHAIN 386 MINER - Network Client
 * 
 * Simple HTTP client for attestation submission
 * No TLS required (HTTP only for vintage hardware)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#include "network.h"
#include "wallet.h"
#include "entropy.h"
#include "fingerprint.h"

/* Initialize network */
int network_init(void) {
    /* Test basic network connectivity */
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return 0;
    }
    
    /* Try to resolve rustchain.org */
    struct hostent *host = gethostbyname("rustchain.org");
    if (!host) {
        close(sock);
        return 0;
    }
    
    close(sock);
    return 1;
}

/* HTTP POST request */
int http_post(const char *host, int port, const char *path, 
              const char *data, char *response, size_t resp_size) {
    int sock;
    struct sockaddr_in server_addr;
    struct hostent *server;
    char request[4096];
    int total_sent, bytes_read;
    
    /* Create socket */
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket");
        return 0;
    }
    
    /* Set timeout */
    struct timeval timeout;
    timeout.tv_sec = 30;
    timeout.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));
    
    /* Resolve host */
    server = gethostbyname(host);
    if (!server) {
        fprintf(stderr, "Cannot resolve %s\n", host);
        close(sock);
        return 0;
    }
    
    /* Set up server address */
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    memcpy(&server_addr.sin_addr.s_addr, server->h_addr, server->h_length);
    
    /* Connect */
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        close(sock);
        return 0;
    }
    
    /* Build HTTP request */
    snprintf(request, sizeof(request),
        "POST %s HTTP/1.0\r\n"
        "Host: %s\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %zu\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s",
        path, host, strlen(data), data);
    
    /* Send request */
    total_sent = 0;
    while (total_sent < (int)strlen(request)) {
        int sent = send(sock, request + total_sent, 
                       strlen(request) - total_sent, 0);
        if (sent < 0) {
            perror("send");
            close(sock);
            return 0;
        }
        total_sent += sent;
    }
    
    /* Read response */
    memset(response, 0, resp_size);
    bytes_read = 0;
    while (1) {
        int n = recv(sock, response + bytes_read, resp_size - bytes_read - 1, 0);
        if (n <= 0) break;
        bytes_read += n;
        if (bytes_read >= (int)resp_size - 1) break;
    }
    response[bytes_read] = '\0';
    
    close(sock);
    
    /* Check for success */
    if (strstr(response, "200 OK") || strstr(response, "201 Created")) {
        return 1;
    }
    
    return 0;
}

/* Submit attestation */
int submit_attestation(const char *host, int port, const char *json) {
    char response[4096];
    return http_post(host, port, "/attest/submit", json, response, sizeof(response));
}

/* Build attestation JSON */
void build_attestation_json(const void *wallet_ptr, 
                           const void *fingerprint_ptr,
                           const void *entropy_ptr,
                           char *buffer,
                           size_t buffer_size) {
    const Wallet386 *wallet = (const Wallet386 *)wallet_ptr;
    const Fingerprint386 *fp = (const Fingerprint386 *)fingerprint_ptr;
    const Entropy386 *entropy = (const Entropy386 *)entropy_ptr;
    
    /* Build hash string */
    char hash_str[65];
    for (int i = 0; i < 32; i++) {
        sprintf(hash_str + i*2, "%02x", entropy->hash[i]);
    }
    hash_str[64] = '\0';
    
    /* Build JSON manually (no JSON library on 386) */
    snprintf(buffer, buffer_size,
        "{"
        "\"miner\":\"%s\","
        "\"miner_id\":\"%s\","
        "\"nonce\":%lu,"
        "\"device\":{"
            "\"arch\":\"%s\","
            "\"family\":\"%s\","
            "\"model\":\"%s\","
            "\"cpu_signature\":\"0x%08lX\","
            "\"bios_date\":\"%s\","
            "\"has_fpu\":%s,"
            "\"isa_timing_cycles\":%lu,"
            "\"mem_timing_cycles\":%lu,"
            "\"clock_drift_ppm\":%lu"
        "},"
        "\"entropy_hash\":\"%s\","
        "\"dev_fee\":{"
            "\"enabled\":true,"
            "\"wallet\":\"founder_dev_fund\","
            "\"amount\":0.001"
        "}"
        "}",
        wallet->wallet_id,
        wallet->miner_id,
        (unsigned long)time(NULL),
        fp->arch,
        fp->family,
        fp->model,
        fp->cpu_signature,
        fp->bios_date,
        fp->has_fpu ? "true" : "false",
        fp->isa_timing_cycles,
        fp->mem_timing_cycles,
        fp->clock_drift_ppm,
        hash_str
    );
}
