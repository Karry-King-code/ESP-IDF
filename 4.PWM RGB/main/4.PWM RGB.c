 #include <stdio.h>
  #include "freertos/FreeRTOS.h"
  #include "freertos/task.h"
  #include "esp_log.h"
  #include "rgb_set.h"
  #include "key_set.h"

  #define DUTY_STEP 100

  void app_main(void)
  {
      rgb_init();
      key_init();

      uint16_t r_duty = 0;
      uint16_t g_duty = 0;
      uint16_t b_duty = 0;
      rgb_set_color(r_duty, g_duty, b_duty);

      ESP_LOGI("PWM", "PWM RGB Example");

      while (1) {
          uint8_t key = key_value_read();

          switch (key) {
              case 1:
                  if (r_duty + DUTY_STEP > RGB_DUTY_MAX) {
                      r_duty = 0;
                  } else {
                      r_duty = r_duty + DUTY_STEP;
                  }
                  rgb_set_color(r_duty, g_duty, b_duty);
                  ESP_LOGI("PWM", "R:%d G:%d B:%d", r_duty, g_duty, b_duty);
                  break;

              case 2:
                  if (g_duty + DUTY_STEP > RGB_DUTY_MAX) {
                      g_duty = 0;
                  } else {
                      g_duty = g_duty + DUTY_STEP;
                  }
                  rgb_set_color(r_duty, g_duty, b_duty);
                  ESP_LOGI("PWM", "R:%d G:%d B:%d", r_duty, g_duty, b_duty);
                  break;

              case 3:
                  if (b_duty + DUTY_STEP > RGB_DUTY_MAX) {
                      b_duty = 0;
                  } else {
                      b_duty = b_duty + DUTY_STEP;
                  }
                  rgb_set_color(r_duty, g_duty, b_duty);
                  ESP_LOGI("PWM", "R:%d G:%d B:%d", r_duty, g_duty, b_duty);
                  break;

              default:
                  break;
          }

          vTaskDelay(pdMS_TO_TICKS(10));
      }
  }