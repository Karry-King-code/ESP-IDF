idf_component_register(SRCS "data_set.c"
                    INCLUDE_DIRS "include"
                    REQUIRES lwip esp_netif esp_http_client cjson mbedtls task_set
                    PRIV_REQUIRES espressif__esp_lvgl_adapter)
