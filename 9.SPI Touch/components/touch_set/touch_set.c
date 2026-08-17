#include "touch_set.h"
#include "esp_lcd_touch_xpt2046.h"
#include "esp_lcd_panel_io.h"
#include "driver/spi_master.h"

static esp_lcd_touch_handle_t touch_handle = NULL;

void touch_init(void)
{
    // 初始化 SPI 总线（使用 SPI3，LCD 用 SPI2，避免冲突）
    // 注意：ESP32-S3 的 SPI0/SPI1 被 Flash/PSRAM 占用，只能用 SPI2/SPI3
    spi_bus_config_t bus_cfg = {
        .sclk_io_num = TOUCH_CLK_PIN,
        .mosi_io_num = TOUCH_DIN_PIN,
        .miso_io_num = TOUCH_DO_PIN,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 64,
    };
    spi_bus_initialize(SPI3_HOST, &bus_cfg, SPI_DMA_CH_AUTO);

    // 创建 SPI 面板 IO
    esp_lcd_panel_io_handle_t io_handle = NULL;
    esp_lcd_panel_io_spi_config_t io_config = ESP_LCD_TOUCH_IO_SPI_XPT2046_CONFIG(TOUCH_CS_PIN);
    esp_lcd_new_panel_io_spi((esp_lcd_spi_bus_handle_t)SPI3_HOST, &io_config, &io_handle);

    // XPT2046 触摸配置
    esp_lcd_touch_config_t touch_cfg = {
        .x_max = TOUCH_WIDTH,
        .y_max = TOUCH_HEIGHT,
        .rst_gpio_num = GPIO_NUM_NC,
        .int_gpio_num = TOUCH_IRQ_PIN,
        .levels = {
            .reset = 0,
            .interrupt = 0,
        },
        .flags = {
            .swap_xy = 1,
            .mirror_x = 0,
            .mirror_y = 0,
        },
    };

    esp_lcd_touch_new_spi_xpt2046(io_handle, &touch_cfg, &touch_handle);
}

bool touch_read(touch_dev_t *data)
{
    data->pressed = false;
    if (touch_handle == NULL) return false;

    esp_lcd_touch_read_data(touch_handle);

    uint16_t x[1], y[1], strength[1];
    uint8_t point_num = 0;
    bool touched = esp_lcd_touch_get_coordinates(touch_handle, x, y, strength, &point_num, 1);

    if (touched && point_num > 0) {
        data->x = x[0];
        data->y = y[0];
        data->pressed = true;
        return true;
    }
    return false;
}