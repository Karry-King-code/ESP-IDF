#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "lcd_set.h"

// RGB565 颜色定义
#define COLOR_RED     0xF800
#define COLOR_GREEN   0x07E0
#define COLOR_BLUE    0x001F
#define COLOR_WHITE   0xFFFF
#define COLOR_BLACK   0x0000

void app_main(void)
{
    lcd_dev_t lcd_dev;
    lcd_init(&lcd_dev);

    ESP_LOGI("LCD", "LCD init done, starting color sweep");

    while (1) {
        // 红色
        lcd_fill_color(&lcd_dev, COLOR_RED);
        ESP_LOGI("LCD", "RED");
        // 绿色
        lcd_fill_color(&lcd_dev, COLOR_GREEN);
        ESP_LOGI("LCD", "GREEN");
        // 蓝色
        lcd_fill_color(&lcd_dev, COLOR_BLUE);
        ESP_LOGI("LCD", "BLUE");
    }
}