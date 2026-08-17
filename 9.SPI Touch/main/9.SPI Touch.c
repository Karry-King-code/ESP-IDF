#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "lcd_set.h"
#include "touch_set.h"

#define COLOR_WHITE 0xFFFF

void app_main(void)
{
    // 初始化 LCD
    lcd_dev_t lcd_dev;
    lcd_init(&lcd_dev);

    // 白色背景
    lcd_fill_color(&lcd_dev, COLOR_WHITE);

    // 初始化触摸屏
    touch_init();

    ESP_LOGI("Touch", "Touch test started, touch the screen");

    while (1) {
        touch_dev_t touch;
        if (touch_read(&touch)) {
            ESP_LOGI("Touch", "X:%d Y:%d", touch.x, touch.y);
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}