extends Control

var myTween : Tween
var Menu_control : Control

var check_debug : = true

onready var display_mode_button = $"Display mode/Options/OptionButton"

var display_mode = {
	0:"Window with borders",
	1:"Window without borders",
	2:"Fullscreen",
}
func _ready():
	myTween = $Tween
	Menu_control = get_parent()
	
	for key in display_mode.keys():
		display_mode_button.add_item(display_mode[key],key)

var position_out_right = Vector2(1024,0)
var position_out_top = Vector2(0,-1024)
var position_center = Vector2(0,0)


#func enter_right():
#	visible = true
#	var _value = myTween.interpolate_property(self,"rect_position",position_out_right,position_center,0.1)
#	_value = myTween.interpolate_callback(self,0.1,"true_visible")
#	_value = myTween.start()
#
#func exit_right():
#	visible = true
#	var _value = myTween.interpolate_property(self,"rect_position",position_center,position_out_right,0.1)
#	_value = myTween.interpolate_callback(self,0.1,"false_visible")
#	_value = myTween.start()
#
#func exit_top():
#	visible = true
#	var _value = myTween.interpolate_property(self,"rect_position",position_center,position_out_top,0.1)
#	_value = myTween.interpolate_callback(self,0.1,"false_visible")
#	_value = myTween.start()
#
#func false_visible():
#	visible = false
#
#func true_visible():
#	visible = true
	
func _on_Debug_pressed():
	global_var.is_debug = $Debug/Check/Debug.pressed
	global_signal.emit_signal("on_change_debug",$Debug/Check/Debug.pressed)

func _on_OptionButton_item_selected(index):
	match (display_mode[index]):
		"Fullscreen":
			OS.window_fullscreen = true
			OS.window_borderless = false
		"Window with borders":
			OS.window_fullscreen = false
			OS.window_borderless = false
			OS.window_maximized = true
		"Window without borders":
			OS.window_fullscreen = false
			OS.window_borderless = true
			OS.window_maximized = true


func _on_Back_pressed():
	Menu_control.travel(Menu_control.PAUSE)
