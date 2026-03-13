/**
 * Network Stack Implementation
 * 
 * Supports:
 * - RR-Net Ethernet cartridge (recommended)
 * - Userport + ESP32 bridge (alternative)
 */

#include "network.h"
#include <stdio.h>
#include <string.h>

#ifdef USE_RRNET
#include <tcpip.h>
#include <socket.h>
#endif

#define SERVER_HOST "rustchain.org"
#define SERVER_PORT 80

static int sockfd = -1;

int network_init(void) {
#ifdef USE_RRNET
    // Initialize RR-Net TCP/IP stack
    if (tcpip_init() != 0) {
        return -1;
    }
#else
    // Initialize Userport + ESP32 bridge
    // This would use RS-232 at 9600 baud
    // Implementation depends on specific hardware
#endif
    return 0;
}

int network_connect(void) {
#ifdef USE_RRNET
    struct sockaddr_in server;
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        return -1;
    }
    
    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);
    // Note: Would need DNS resolution or hardcoded IP
    
    if (connect(sockfd, (struct sockaddr*)&server, sizeof(server)) < 0) {
        close(sockfd);
        sockfd = -1;
        return -1;
    }
    
    return 0;
#else
    // Userport + ESP32 connection
    // Open RS-232 at 9600 baud
    // Send connection command to ESP32
    return 0;  // Placeholder
#endif
}

int network_send(const char* data, int len) {
#ifdef USE_RRNET
    if (sockfd < 0) {
        return -1;
    }
    return send(sockfd, data, len, 0);
#else
    // Send via RS-232 to ESP32
    return len;  // Placeholder
#endif
}

int network_recv(char* buffer, int max_len) {
#ifdef USE_RRNET
    if (sockfd < 0) {
        return -1;
    }
    return recv(sockfd, buffer, max_len, 0);
#else
    // Receive via RS-232 from ESP32
    return 0;  // Placeholder
#endif
}

void network_close(void) {
#ifdef USE_RRNET
    if (sockfd >= 0) {
        close(sockfd);
        sockfd = -1;
    }
#else
    // Close RS-232 connection
#endif
}

int http_post(const char* path, const char* json_body, char* response, int max_response_len) {
    char request[512];
    int body_len = strlen(json_body);
    
    // Build HTTP request
    snprintf(request, sizeof(request),
        "POST %s HTTP/1.0\r\n"
        "Host: " SERVER_HOST "\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "\r\n"
        "%s",
        path, body_len, json_body
    );
    
    // Send request
    int sent = network_send(request, strlen(request));
    if (sent < 0) {
        return -1;
    }
    
    // Receive response
    int received = network_recv(response, max_response_len);
    if (received < 0) {
        return -1;
    }
    
    // Find body (skip HTTP headers)
    char* body = strstr(response, "\r\n\r\n");
    if (body) {
        memmove(response, body + 4, strlen(body + 4) + 1);
    }
    
    return 0;
}
