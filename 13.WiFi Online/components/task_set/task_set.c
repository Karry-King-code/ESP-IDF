#include "task_set.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

app_set_t app = {
    .uart = {
        .tx_data = "",
        .rx_data = {0},
        .handle = NULL
    },
    .setting = {
        .screen_light = 100,
        .wifi_status = 0,
        .wifi_scan = true,
        .wifi_ssid = {'\0'},
        .wifi_password = NULL,
        .wifi_networks = NULL,
        .wifi_connect = false,
        .wifi_disconnect = false,
        .wifi_failure = 0,
        .handle = NULL
    },
    .data = {
        .time_init = false,
        .weather_update = false,
        .handle = NULL
    }
};

void task_init(void)
{
    task_create(&app.setting.handle, wifi_task, "wifi_task", 1024 * 6);
    task_create(&app.data.handle, data_task, "data_task", 1024 * 6);
}

void task_create(TaskHandle_t *handle, TaskFunction_t func, const char *name, uint32_t stack)
{
    if (*handle == NULL) {
        xTaskCreatePinnedToCore(func, name, stack, NULL, 1, handle, 0);
    }
}

void task_delete(TaskHandle_t *handle)
{
    if (*handle != NULL) {
        vTaskDelete(*handle);
        *handle = NULL;
    }
}