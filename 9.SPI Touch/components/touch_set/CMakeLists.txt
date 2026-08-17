idf_component_register(SRCS "touch_set.c"
                    INCLUDE_DIRS "include"
                    REQUIRES esp_driver_gpio esp_driver_spi
                    PRIV_REQUIRES atanisoft__esp_lcd_touch_xpt2046)
