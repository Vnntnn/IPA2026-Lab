#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <regex>
#include <libssh2.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

std::string
read_until_prompt(LIBSSH2_CHANNEL* channel, const std::string& pattern, int timeout_ms = 5000)
{
    std::string buffer;
    char char_buf[128];
    auto start_time = std::chrono::steady_clock::now();
    std::regex prompt_regex(pattern);

    while (true) {
        int rc = libssh2_channel_read(channel, char_buf, sizeof(char_buf) - 1);
        if (rc > 0) {
            char_buf[rc] = '\0';
            buffer += char_buf;

            if (std::regex_search(buffer, prompt_regex)) {
                break;
            }
        }
        
        auto current_time = std::chrono::steady_clock::now();
        if (std::chrono::duration_cast<std::chrono::milliseconds>(current_time - start_time).count() > timeout_ms) {
            std::cout << "[Warning] Timeout reached waiting for prompt.\n";
            break;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
    return buffer;
}

void 
send_command_line(LIBSSH2_CHANNEL* channel, const std::string& command)
{
    std::string full_cmd = command + "\n";
    libssh2_channel_write(channel, full_cmd.c_str(), full_cmd.length());
}

int
main()
{
    const std::string host = ""; // IP or Hostname
    const int port = 22;
    const std::string username = "admin";
    const std::string password = "cisco";
    
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in sin;
    sin.sin_family = AF_INET;
    sin.sin_port = htons(port);
    sin.sin_addr.s_addr = inet_addr(host.c_str());
    
    if (connect(sock, (struct sockaddr*)(&sin), sizeof(struct sockaddr_in)) != 0) {
        std::cerr << "Failed to connect to host socket.\n";
        return -1;
    }

    libssh2_init(0);
    LIBSSH2_SESSION* session = libssh2_session_init();
    if (libssh2_session_handshake(session, sock)) {
        std::cerr << "SSH handshake failed.\n";
        return -1;
    }

    if (libssh2_userauth_password(session, username.c_str(), password.c_str())) {
        std::cerr << "Authentication failed.\n";
        return -1;
    }

    LIBSSH2_CHANNEL* channel = libssh2_channel_open_session(session);
    if (libssh2_channel_request_pty(channel, "vt100") || libssh2_channel_shell(channel)) {
        std::cerr << "Failed to open interactive shell pty.\n";
        return -1;
    }

    std::string prompt_pattern = "#"; 
    std::cout << read_until_prompt(channel, prompt_pattern);

    send_command_line(channel, "configure terminal");
    std::cout << read_until_prompt(channel, "\\(config\\)#");

    send_command_line(channel, "interface GigabitEthernet0/1");
    std::cout << read_until_prompt(channel, "\\(config-if\\)#");

    send_command_line(channel, "no shutdown");
    std::cout << read_until_prompt(channel, "\\(config-if\\)#");

    send_command_line(channel, "end");
    std::cout << read_until_prompt(channel, "#");

    // Cleanup tunnel
    libssh2_channel_free(channel);
    libssh2_session_disconnect(session, "Normal Shutdown");
    libssh2_session_free(session);
    close(sock);
    libssh2_exit();
    std::cout << "[Configuration done.]";

    return 0;
}
