idf_component_register(SRCS "rgb_set.c"
                    INCLUDE_DIRS "include"
                    REQUIRES esp_driver_gpio
                    REQUIRES esp_driver_ledc)
