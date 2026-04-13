# Antes de rodar esse código, instale a biblioteca easygui!
import easygui

max_sensors = 4
limit_temp = 38.0
failed_sensors_count = 0
report_log = "# RELATÓRIO DE FALHAS (ALTA TEMPERATURA)\n"

gui_title = "Monitor v1.0"

easygui.msgbox(f"Iniciando a checagem de {max_sensors} sensores...", title=gui_title)

for i in range(1, max_sensors + 1):
    # O enterbox pede o dado de cada sensor
    input_value = easygui.enterbox(
        msg=f"Digite a temperatura do Sensor {i} (°C):",
        title=gui_title
    )

    # Se o usuário cancelar a janela, paramos o teste
    if input_value is None:
        break

    temp = float(input_value)

    # Lógica de Engenharia: Se passar do limite, "anotamos" no relatório
    if temp > limit_temp:
        failed_sensors_count += 1
        report_log += f"* Sensor {i}: {temp}°C (ACIMA DO LIMITE)\n"

# Finalização: Se houver erros, o easygui mostra o relatório completo de uma vez
if failed_sensors_count > 0:
    easygui.codebox(
        msg=f"Atenção! {failed_sensors_count} sensores falharam no teste:",
        title="LOG DE ERROS",
        text=report_log
    )
else:
    easygui.msgbox("Todos os sensores operando em temperatura normal.", title=gui_title)