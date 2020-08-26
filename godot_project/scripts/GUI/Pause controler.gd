extends MarginContainer


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var myTween : Tween
var Menu_control : Control
# Called when the node enters the scene tree for the first time.
func _ready():
	myTween = $Tween
	Menu_control = get_parent()
#	GUI_control = get_tree().get_nodes_in_group("GUI control")[0]
#	pass # Replace with function body.
#
#var position_out_top = Vector2(0,-1024)
#var position_out_left = Vector2(-1024,0)
#var position_center = Vector2(0,0)
## Called every frame. 'delta' is the elapsed time since the previous frame.
#
#
#func enter_top():
#	visible = true
#	var _value = myTween.interpolate_property(self,"rect_position",position_out_top,position_center,0.1)
#	_value = myTween.interpolate_callback(self,0.1,"true_visible")
#	_value = myTween.start()
#
#func enter_left():
#	visible = true
#	var _value = myTween.interpolate_property(self,"rect_position",position_out_left,position_center,0.1)
#	_value = myTween.interpolate_callback(self,0.1,"true_visible")
#	_value = myTween.start()
#
#func exit_top():
#	visible = true
#	var _value = myTween.interpolate_property(self,"rect_position",position_center,position_out_top,0.1)
#	_value = myTween.interpolate_callback(self,0.1,"false_visible")
#	_value = myTween.start()
#
#func exit_left():
#	visible = true
#	var _value = myTween.interpolate_property(self,"rect_position",position_center,position_out_left,0.1)
#	_value = myTween.interpolate_callback(self,0.1,"false_visible")
#	_value = myTween.start()
#
#func false_visible():
#	visible = false
#
#func true_visible():
#	visible = true
	
func _on_Exit_pressed():
	get_tree().quit()


func _on_Continue_pressed():
	get_tree().paused = false
	Menu_control.travel(Menu_control.NONE)


func _on_Settings_pressed():
	Menu_control.travel(Menu_control.SETTINGS)


func _on_Main_menu_pressed():
	var _err = get_tree().change_scene("res://scenes/Title Screen.tscn")
