#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "uart_set.h"
#include "rgb_set.h"

static uint16_t r_state = 0;
static uint16_t g_state = 0;
static uint16_t b_state = 0;

static const char *TAG = "UART_RGB";

static void print_status(void)
{
    char status[64];
    snprintf(status, sizeof(status), "Red:%s Green:%s Blue:%s\r\n",
             r_state ? "ON" : "OFF",
             g_state ? "ON" : "OFF",
             b_state ? "ON" : "OFF");
    uart_write_bytes(UART_PORT_NUM, status, strlen(status));
}

static void print_unknown(const char *cmd, int len)
{
    char msg[80];
    int n = snprintf(msg, sizeof(msg), "[%.*s] NOT RECOGNIZED\r\n", len, cmd);
    uart_write_bytes(UART_PORT_NUM, msg, n);
}

void app_main(void)
{
    rgb_init();
    uart_init();
    rgb_set_color(r_state, g_state, b_state);

    // 🔍 调试 0:启动确认
    ESP_LOGI(TAG, "UART RGB Example");
    ESP_LOGI(TAG, "Try commands: R ON / R OFF / G ON / G OFF / B ON / B OFF / A ON / A OFF");

    char buf[64] = {0};

    while (1) {
        int len = uart_read_bytes(UART_PORT_NUM, buf, sizeof(buf) - 1, 50 / portTICK_PERIOD_MS);
        if (len > 0) {
            // 🔍 调试 1:看到 UART 收到的原始字节(十六进制)
            ESP_LOGI(TAG, "RX %d bytes:", len);
            for (int i = 0; i < len && i < 32; i++) {
                ESP_LOGI(TAG, "  buf[%d] = 0x%02x (%c)", i, buf[i],
                         (buf[i] >= 32 && buf[i] <= 126) ? buf[i] : '.');
            }

            buf[len] = '\0';
            // 去掉尾部 \r \n，方便匹配 "R ON" 这种命令
            while (len > 0 && (buf[len - 1] == '\r' || buf[len - 1] == '\n')) {
                buf[--len] = '\0';
            }

            // 🔍 调试 2:看到去除 \r\n 后的命令字符串
            ESP_LOGI(TAG, "CMD after strip: [%s] (len=%d)", buf, len);

            if (strcmp(buf, "R ON") == 0) {
                r_state = RGB_DUTY_MAX;
            } else if (strcmp(buf, "R OFF") == 0) {
                r_state = 0;
            } else if (strcmp(buf, "G ON") == 0) {
                g_state = RGB_DUTY_MAX;
            } else if (strcmp(buf, "G OFF") == 0) {
                g_state = 0;
            } else if (strcmp(buf, "B ON") == 0) {
                b_state = RGB_DUTY_MAX;
            } else if (strcmp(buf, "B OFF") == 0) {
                b_state = 0;
            } else if (strcmp(buf, "A ON") == 0) {
                r_state = RGB_DUTY_MAX;
                g_state = RGB_DUTY_MAX;
                b_state = RGB_DUTY_MAX;
            } else if (strcmp(buf, "A OFF") == 0) {
                r_state = 0;
                g_state = 0;
                b_state = 0;
            } else {
                print_unknown(buf, len);
                continue;
            }

            memset(buf, 0, sizeof(buf));
            rgb_set_color(r_state, g_state, b_state);
            print_status();
        }
    }
}