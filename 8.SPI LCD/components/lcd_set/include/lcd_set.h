#ifndef LCD_SET_H
#define LCD_SET_H

#include "esp_err.h"
#include "esp_lcd_types.h"
#include "driver/gpio.h"

// LCD 引脚定义
#define LCD_SCK_PIN     GPIO_NUM_12
#define LCD_MOSI_PIN    GPIO_NUM_11
#define LCD_MISO_PIN    GPIO_NUM_13
#define LCD_CS_PIN      GPIO_NUM_10
#define LCD_DC_PIN      GPIO_NUM_9
#define LCD_LED_PIN     GPIO_NUM_14
#define LCD_RST_PIN     GPIO_NUM_NC

// LCD 分辨率
#define LCD_WIDTH       320
#define LCD_HEIGHT      240

// LCD 句柄类型
typedef struct {
    esp_lcd_panel_handle_t panel;
} lcd_dev_t;

/**
 * @brief 初始化 LCD（ST7789，SPI2，横屏 320x240）
 *
 * @param lcd_dev LCD 设备结构体指针
 */
void lcd_init(lcd_dev_t *lcd_dev);

/**
 * @brief 刷新 LCD 显示区域（供 LVGL 调用）
 *
 * @param lcd_dev LCD 设备结构体指针
 * @param x_start 起始 X 坐标
 * @param y_start 起始 Y 坐标
 * @param x_end 结束 X 坐标
 * @param y_end 结束 Y 坐标
 * @param color_data 颜色数据缓冲区（RGB565 格式）
 */
void lcd_flush(lcd_dev_t *lcd_dev, int x_start, int y_start, int x_end, int y_end, const uint16_t *color_data);

/**
 * @brief 填充整个屏幕为单一颜色
 *
 * @param lcd_dev LCD 设备结构体指针
 * @param color 颜色值（RGB565 格式）
 */
void lcd_fill_color(lcd_dev_t *lcd_dev, uint16_t color);

#endif /* LCD_SET_H */
