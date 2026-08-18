#include "touch_set.h"
#include "esp_lcd_touch_xpt2046.h"
#include "esp_lcd_panel_io.h"
#include "driver/spi_master.h"

static esp_lcd_touch_handle_t touch_handle = NULL;

void touch_init(touch_dev_t *dev)
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
        .int_gpio_num = GPIO_NUM_NC, // 不用中断:IRQ 模式只能检测按下、检测不到松开,会导致按键永远不触发 CLICKED;轮询模式最稳
        .levels = {
            .reset = 0,
            .interrupt = 0,
        },
        .flags = {
            .swap_xy = 1,    // 教材假设 X 沿 320 侧(y_max=240);你面板实际可能是 X 沿 240 侧,改成 swap_xy=0 试试
            .mirror_x = 0,   // 如果还不对,改 mirror_x=1 水平镜像
            .mirror_y = 0,
        },
    };

    esp_lcd_touch_new_spi_xpt2046(io_handle, &touch_cfg, &touch_handle);
    dev->handle = touch_handle;  // 新增：存储触摸句柄
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

// 自定义触摸读取:驱动算出坐标(含镜像/翻转)后,叠加校准偏移和缩放。
// 传给 esp_lvgl_adapter 的 touch_cfg.callbacks.custom_touch_read。
esp_err_t touch_read_calibrated(esp_lcd_touch_handle_t handle,
                                esp_lcd_touch_point_data_t *points,
                                uint8_t *count, uint8_t max_count, void *user_ctx)
{
    esp_lcd_touch_read_data(handle);
    esp_err_t ret = esp_lcd_touch_get_data(handle, points, count, max_count);
    if (ret != ESP_OK) {
        return ret;
    }

    for (uint8_t i = 0; i < *count; i++) {
        int x = (int)((float)points[i].x * TOUCH_CAL_SCALE_X + TOUCH_CAL_OFFSET_X);
        int y = (int)((float)points[i].y * TOUCH_CAL_SCALE_Y + TOUCH_CAL_OFFSET_Y);
        if (x < 0) x = 0;
        if (x > TOUCH_WIDTH) x = TOUCH_WIDTH;
        if (y < 0) y = 0;
        if (y > TOUCH_HEIGHT) y = TOUCH_HEIGHT;
        points[i].x = (uint16_t)x;
        points[i].y = (uint16_t)y;
    }
    return ESP_OK;
}