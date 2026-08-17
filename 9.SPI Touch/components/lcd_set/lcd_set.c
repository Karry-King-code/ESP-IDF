#include "lcd_set.h"
#include "esp_lcd_panel_io.h"
#include "esp_lcd_panel_ops.h"
#include "esp_lcd_panel_vendor.h"
#include "driver/spi_master.h"
#include "driver/gpio.h"
#include "esp_heap_caps.h"

void lcd_init(lcd_dev_t *lcd_dev)
{
    // 初始化 SPI 总线
    spi_bus_config_t bus_cfg = {
        .sclk_io_num = LCD_SCK_PIN,
        .mosi_io_num = LCD_MOSI_PIN,
        .miso_io_num = LCD_MISO_PIN,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = LCD_WIDTH * LCD_HEIGHT * sizeof(uint16_t),
    };
    spi_bus_initialize(SPI2_HOST, &bus_cfg, SPI_DMA_CH_AUTO);

    // 创建 SPI LCD 面板 IO
    esp_lcd_panel_io_handle_t io_handle = NULL;
    esp_lcd_panel_io_spi_config_t io_config = {
        .dc_gpio_num = LCD_DC_PIN,
        .cs_gpio_num = LCD_CS_PIN,
        .pclk_hz = 40 * 1000 * 1000,
        .lcd_cmd_bits = 8,
        .lcd_param_bits = 8,
        .spi_mode = 0,
        .trans_queue_depth = 10,
    };
    esp_lcd_new_panel_io_spi((esp_lcd_spi_bus_handle_t)SPI2_HOST, &io_config, &io_handle);

    // 创建 LCD 面板（ST7789）
    esp_lcd_panel_handle_t panel_handle = NULL;
    esp_lcd_panel_dev_config_t panel_config = {
        .reset_gpio_num = LCD_RST_PIN,
        .rgb_endian = LCD_RGB_ENDIAN_RGB,
        .bits_per_pixel = 16,
    };
    esp_lcd_new_panel_st7789(io_handle, &panel_config, &panel_handle);

    // 初始化面板
    esp_lcd_panel_reset(panel_handle);
    esp_lcd_panel_init(panel_handle);

    // 设置横屏
    esp_lcd_panel_swap_xy(panel_handle, true);
    esp_lcd_panel_mirror(panel_handle, false, false);

    // 开启显示
    esp_lcd_panel_disp_on_off(panel_handle, true);

    // 配置背光引脚
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << LCD_LED_PIN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);
    gpio_set_level(LCD_LED_PIN, 1);

    lcd_dev->panel = panel_handle;
}

void lcd_flush(lcd_dev_t *lcd_dev, int x_start, int y_start, int x_end, int y_end, const uint16_t *color_data)
{
    esp_lcd_panel_draw_bitmap(lcd_dev->panel, x_start, y_start, x_end, y_end, color_data);
}

void lcd_fill_color(lcd_dev_t *lcd_dev, uint16_t color)
{
    uint16_t *buffer = heap_caps_malloc(LCD_WIDTH * sizeof(uint16_t), MALLOC_CAP_DMA);
    for (int i = 0; i < LCD_WIDTH; i++) {
        buffer[i] = color;
    }
    for (int y = 0; y < LCD_HEIGHT; y++) {
        esp_lcd_panel_draw_bitmap(lcd_dev->panel, 0, y, LCD_WIDTH, y + 1, buffer);
    }
}