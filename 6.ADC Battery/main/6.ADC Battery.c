#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "adc_set.h"

void app_main(void)
{
    adc_init();
    ESP_LOGI("Battery", "ADC Battery Example");

    while (1) {
        float voltage = adc_get_battery_voltage();
        uint8_t percent = adc_get_battery_percent(voltage);
        ESP_LOGI("Battery", "Voltage: %.3fV, Percent: %d%%", voltage, percent);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}