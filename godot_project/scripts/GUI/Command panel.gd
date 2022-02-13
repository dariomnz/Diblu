extends Control

onready var command_line = $"Command line"
onready var command_history_panel = $"Command history panel"


# Called when the node enters the scene tree for the first time.
func _ready():
	command_line.text = ""
	command_history_panel.text = ""
	


func _on_LineEdit_text_entered(new_text:String):
	if new_text.empty():
		return
		
	command_line.text = ""
	command_history_panel.text += new_text + "\n"
	command_history_panel.scroll_vertical = 9999999
