#include <stdio.h>
  #include "freertos/FreeRTOS.h"
  #include "freertos/task.h"
  #include "esp_log.h"
  #include "rgb_set.h"
  #include "key_set.h"

  void app_main(void)
  {
      rgb_init();
      key_init();

      uint8_t color = RGB_COLOR_OFF;
      rgb_set_color(color);

      ESP_LOGI("Key", "GPIO Key Example");

      while (1) {
          uint8_t key = key_value_read();

          switch (key) {
              case 1:
                  if (color & RGB_COLOR_RED) {
                      color = color & ~RGB_COLOR_RED;
                      ESP_LOGI("Key", "RED OFF");
                  } else {
                      color = color | RGB_COLOR_RED;
                      ESP_LOGI("Key", "RED ON");
                  }
                  rgb_set_color(color);
                  break;

              case 2:
                  if (color & RGB_COLOR_GREEN) {
                      color = color & ~RGB_COLOR_GREEN;
                      ESP_LOGI("Key", "GREEN OFF");
                  } else {
                      color = color | RGB_COLOR_GREEN;
                      ESP_LOGI("Key", "GREEN ON");
                  }
                  rgb_set_color(color);
                  break;

              case 3:
                  if (color & RGB_COLOR_BLUE) {
                      color = color & ~RGB_COLOR_BLUE;
                      ESP_LOGI("Key", "BLUE OFF");
                  } else {
                      color = color | RGB_COLOR_BLUE;
                      ESP_LOGI("Key", "BLUE ON");
                  }
                  rgb_set_color(color);
                  break;

              default:
                  break;
          }

          vTaskDelay(pdMS_TO_TICKS(10));
      }
  }