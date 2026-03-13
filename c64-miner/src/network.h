/**
 * Network Stack Interface
 */

#ifndef NETWORK_H
#define NETWORK_H

// Initialize network stack
int network_init(void);

// Connect to server
int network_connect(void);

// Send data
int network_send(const char* data, int len);

// Receive data
int network_recv(char* buffer, int max_len);

// Close connection
void network_close(void);

// HTTP POST request
int http_post(const char* path, const char* json_body, char* response, int max_response_len);

#endif
