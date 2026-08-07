#include <stdio.h>
  #include "freertos/FreeRTOS.h"
  #include "freertos/task.h"
  #include "esp_log.h"
  #include "rgb_set.h"

  void app_main(void)
  {
      rgb_init();

      while (1) {
          rgb_set_color(RGB_COLOR_RED);
          ESP_LOGI("RGB", "RED");
          vTaskDelay(pdMS_TO_TICKS(1000));

          rgb_set_color(RGB_COLOR_GREEN);
          ESP_LOGI("RGB", "GREEN");
          vTaskDelay(pdMS_TO_TICKS(1000));

          rgb_set_color(RGB_COLOR_BLUE);
          ESP_LOGI("RGB", "BLUE");
          vTaskDelay(pdMS_TO_TICKS(1000));

          rgb_set_color(RGB_COLOR_YELLOW);
          ESP_LOGI("RGB", "YELLOW");
          vTaskDelay(pdMS_TO_TICKS(1000));

          rgb_set_color(RGB_COLOR_CYAN);
          ESP_LOGI("RGB", "CYAN");
          vTaskDelay(pdMS_TO_TICKS(1000));

          rgb_set_color(RGB_COLOR_MAGENTA);
          ESP_LOGI("RGB", "MAGENTA");
          vTaskDelay(pdMS_TO_TICKS(1000));

          rgb_set_color(RGB_COLOR_WHITE);
          ESP_LOGI("RGB", "WHITE");
          vTaskDelay(pdMS_TO_TICKS(1000));
      }
  }