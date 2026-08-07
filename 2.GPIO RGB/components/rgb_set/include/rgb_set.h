#ifndef RGB_SET_H
#define RGB_SET_H
#include "driver/gpio.h"

// RGB LED 引脚定义
#define RGB_R_PIN  GPIO_NUM_21
#define RGB_G_PIN  GPIO_NUM_47
#define RGB_B_PIN  GPIO_NUM_48

// 预定义颜色（低电平点亮，1 = 亮）
#define RGB_COLOR_RED 0x04 // R=1, G=0, B=0
#define RGB_COLOR_GREEN 0x02 // R=0, G=1, B=0
#define RGB_COLOR_BLUE 0x01 // R=0, G=0, B=1
#define RGB_COLOR_YELLOW (RGB_COLOR_RED | RGB_COLOR_GREEN)
#define RGB_COLOR_CYAN (RGB_COLOR_GREEN | RGB_COLOR_BLUE)
#define RGB_COLOR_MAGENTA (RGB_COLOR_RED | RGB_COLOR_BLUE)
#define RGB_COLOR_WHITE (RGB_COLOR_RED | RGB_COLOR_GREEN | RGB_COLOR_BLUE)
#define RGB_COLOR_OFF 0x00 // 全部关闭

/**
* @brief 初始化 RGB LED
*
* 将 R、G、B 三个引脚配置为 GPIO 输出模式，并默认关闭 LED
*/
void rgb_init(void);
/**
* @brief 设置 RGB LED 颜色
*
* @param color 颜色值，使用 RGB_COLOR_xxx 宏定义，如 RGB_COLOR_RED
*/
void rgb_set_color(uint8_t color);

#endif
