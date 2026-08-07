#include <stdio.h>
#include "rgb_set.h"

void rgb_init(void)
{
// 配置 R、G、B 三个引脚为 GPIO 输出模式
gpio_config_t io_conf = {.pin_bit_mask = (1ULL << RGB_R_PIN) | (1ULL << RGB_G_PIN) | (1ULL <<RGB_B_PIN),
.mode = GPIO_MODE_OUTPUT,
.pull_up_en = GPIO_PULLUP_DISABLE,
.pull_down_en = GPIO_PULLDOWN_DISABLE,
.intr_type = GPIO_INTR_DISABLE,
};
gpio_config(&io_conf);
// 默认关闭 LED
rgb_set_color(RGB_COLOR_OFF);
}

void rgb_set_color(uint8_t color)
{
// 低电平点亮：color 位为 1 时输出低电平（点亮），为 0 时输出高电平（熄灭）
gpio_set_level(RGB_R_PIN, (color & 0x04) ? 0 : 1);
gpio_set_level(RGB_G_PIN, (color & 0x02) ? 0 : 1);
gpio_set_level(RGB_B_PIN, (color & 0x01) ? 0 : 1);
}

