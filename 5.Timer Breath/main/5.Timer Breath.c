#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "rgb_set.h"
#include "key_set.h"
#include "timer_set.h"

// 呼吸灯步进值（每次回调变化的占空比）
#define BREATH_STEP 5

// 红色呼吸灯状态
static uint16_t r_duty = 0;
static int8_t r_dir = 1;        // 1=渐亮，-1=渐暗
static uint8_t r_breathing = 0; // 0=停止，1=呼吸中

// 绿色呼吸灯状态
static uint16_t g_duty = 0;
static int8_t g_dir = 1;
static uint8_t g_breathing = 0;

// 蓝色呼吸灯状态
static uint16_t b_duty = 0;
static int8_t b_dir = 1;
static uint8_t b_breathing = 0;

// 定时器周期（微秒）
#define TIMER_PERIOD_US 10000  // 10ms

// IRAM_ATTR表示把函数放在IRAM中执行,中断回调要求执行速度快比Flash 更加快
// 硬件定时器回调函数：每 10ms 更新一次所有正在呼吸的通道
static bool IRAM_ATTR breath_timer_cb(gptimer_handle_t timer,
                                      const gptimer_alarm_event_data_t *edata,
                                      void *user_data)
{
    // 更新红色呼吸
    if (r_breathing) {
        if (r_dir > 0) {
            r_duty += BREATH_STEP;
            if (r_duty >= RGB_DUTY_MAX) {
                r_duty = RGB_DUTY_MAX;
                r_dir = -1;
            }
        } else {
            if (r_duty <= BREATH_STEP) {
                r_duty = 0;
                r_dir = 1;
            } else {
                r_duty -= BREATH_STEP;
            }
        }
    }

    // 更新绿色呼吸
    if (g_breathing) {
        if (g_dir > 0) {
            g_duty += BREATH_STEP;
            if (g_duty >= RGB_DUTY_MAX) {
                g_duty = RGB_DUTY_MAX;
                g_dir = -1;
            }
        } else {
            if (g_duty <= BREATH_STEP) {
                g_duty = 0;
                g_dir = 1;
            } else {
                g_duty -= BREATH_STEP;
            }
        }
    }

    // 更新蓝色呼吸
    if (b_breathing) {
        if (b_dir > 0) {
            b_duty += BREATH_STEP;
            if (b_duty >= RGB_DUTY_MAX) {
                b_duty = RGB_DUTY_MAX;
                b_dir = -1;
            }
        } else {
            if (b_duty <= BREATH_STEP) {
                b_duty = 0;
                b_dir = 1;
            } else {
                b_duty -= BREATH_STEP;
            }
        }
    }

    // 更新 RGB 显示
    rgb_set_color(r_duty, g_duty, b_duty);

    return false;  // 返回 false 表示不需要唤醒高优先级任务
}

void app_main(void)
{
    // 1. 初始化 RGB LED（PWM 模式）和按键
    rgb_init();
    key_init();

    // 2. 创建硬件定时器，周期 10ms
    timer_init(TIMER_PERIOD_US, breath_timer_cb, NULL);

    // 3. 初始状态：全灭
    rgb_set_color(0, 0, 0);

    ESP_LOGI("Breath", "Timer Breath Example");
    ESP_LOGI("Breath", "KEY1: Red  KEY2: Green  KEY3: Blue");

    while (1) {
        uint8_t key = key_value_read();

        switch (key) {
            case 1:  // 按键1：切换红色呼吸
                r_breathing = !r_breathing;
                if (!r_breathing) {
                    r_duty = 0;
                }
                ESP_LOGI("Breath", "Red breathing: %s", r_breathing ? "ON" : "OFF");
                break;

            case 2:  // 按键2：切换绿色呼吸
                g_breathing = !g_breathing;
                if (!g_breathing) {
                    g_duty = 0;
                }
                ESP_LOGI("Breath", "Green breathing: %s", g_breathing ? "ON" : "OFF");
                break;

            case 3:  // 按键3：切换蓝色呼吸
                b_breathing = !b_breathing;
                if (!b_breathing) {
                    b_duty = 0;
                }
                ESP_LOGI("Breath", "Blue breathing: %s", b_breathing ? "ON" : "OFF");
                break;

            default:
                break;
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}