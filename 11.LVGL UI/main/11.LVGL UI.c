#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "lcd_set.h"
#include "touch_set.h"
#include "lvgl_set.h"
#include "lvgl.h"
#include "esp_lv_adapter.h"
#include "ui_set.h"

void app_main(void)
{
    lcd_dev_t lcd_dev;
    lcd_init(&lcd_dev);

    touch_dev_t touch_dev;
    touch_init(&touch_dev);

    lvgl_init(&lcd_dev, &touch_dev);

    if (esp_lv_adapter_lock(-1) == ESP_OK) {
        ui_init();
        esp_lv_adapter_unlock();
    }

    ESP_LOGI("LVGL", "UI initialized");

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}