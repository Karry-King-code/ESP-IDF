#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "lcd_set.h"
#include "touch_set.h"
#include "lvgl_set.h"
#include "lvgl.h"
#include "esp_lv_adapter.h"
#include "music/lv_demo_music.h"

void app_main(void)
{
    // 初始化 LCD
    lcd_dev_t lcd_dev;
    lcd_init(&lcd_dev);

    // 初始化触摸屏
    touch_dev_t touch_dev;
    touch_init(&touch_dev);

    // 初始化 LVGL
    lvgl_init(&lcd_dev, &touch_dev);

    // 运行音乐播放器 Demo（需要加锁）
    if (esp_lv_adapter_lock(-1) == ESP_OK) {
        lv_demo_music();
        esp_lv_adapter_unlock();
    }

    ESP_LOGI("LVGL", "Music demo started");

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}