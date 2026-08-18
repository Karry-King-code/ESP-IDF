#ifndef TOUCH_SET_H
#define TOUCH_SET_H

#include "esp_lcd_touch_xpt2046.h"
#include "esp_lcd_panel_io.h"
#include "driver/gpio.h"
#include <stdint.h>
#include <stdbool.h>

// XPT2046 引脚定义
#define TOUCH_CLK_PIN   GPIO_NUM_15
#define TOUCH_CS_PIN    GPIO_NUM_7
#define TOUCH_DIN_PIN   GPIO_NUM_6   // MOSI
#define TOUCH_DO_PIN    GPIO_NUM_5   // MISO
#define TOUCH_IRQ_PIN   GPIO_NUM_4   // 中断引脚

// 屏幕分辨率
#define TOUCH_WIDTH     320
#define TOUCH_HEIGHT    240

// ===== 触摸校准(手调参数)=====
// 现象:点按钮中心没反应,要点按钮的右上角才触发 → 判定点整体偏左下。
// 修法:把判定点向右、向上平移。屏幕坐标 y 轴向下为正,所以"上移"是减 y。
#define TOUCH_CAL_OFFSET_X   60 //判定点右移像素数(正=右)
#define TOUCH_CAL_OFFSET_Y   -60 //判定点上移像素数(负=上)
#define TOUCH_CAL_SCALE_X    1.0f    // 水平缩放(边缘不准时再调,中心不准不用管)
#define TOUCH_CAL_SCALE_Y    1.0f    // 垂直缩放

// 触摸设备结构体
typedef struct {
    uint16_t x;
    uint16_t y;
    bool pressed;
    esp_lcd_touch_handle_t handle;
} touch_dev_t;

/**
 * @brief 初始化触摸设备
 *
 * @param dev 触摸设备指针
 */
void touch_init(touch_dev_t *dev);

/**
* @brief 读取触摸数据
*
* @param data 读取到的触摸数据
* @return true 读取成功
* @return false 读取失败
*/
bool touch_read(touch_dev_t *data);

/**
 * @brief 自定义触摸读取(带校准偏移),给 esp_lvgl_adapter 用
 *
 * @return esp_err_t
 */
esp_err_t touch_read_calibrated(esp_lcd_touch_handle_t handle,
                                esp_lcd_touch_point_data_t *points,
                                uint8_t *count, uint8_t max_count, void *user_ctx);

#endif /* TOUCH_SET_H */