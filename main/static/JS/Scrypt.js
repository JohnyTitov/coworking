var month_count = 0;				// счетчик месяца

var this_select_room = '1'; 		// выбранная комната
let color_time = [];				// цвет временной панели

let red_border = {		// красная граница (область, за которой нельзя перекрашивать панель в черный)
	up: 27,		// нижняя
	down: 0,	// верхняя
};

var time_begin_id = false;			// id времени "с"
var time_end_id = false;			// id времени "до"

let tp_element = {     // элементы панели времени
	begin: "time_begin",  
	end: "time_end",
	tb: "tb_",
	te: "te_",
	lbegin: "label_begin",
	lend: "label_end",
	mobile_begin: "m_time_begin",
	mobile_end: "m_time_end",
	mtb: "mtb_",
	mte: "mte_",
	m_select_begin: "select_mobile_begin",
	m_select_end: "select_mobile_end",
};

function get_id_by_value(radio_time, command){	// функция получения id по значению

	radio_begin = document.getElementsByName("time_begin");
	radio_end = document.getElementsByName("time_end");

	var begin = new Map([]);	// создаём пустой словарь, где каждый эл-т = время: индекс (0 - 27)

	radio_begin.forEach(function(radio, i, radio_begin) {	// в цикле заполняем словарь
  		begin.set(radio.value, i);
	});

	var end = new Map([]);	// создаём пустой словарь, где каждый эл-т = время: индекс (0 - 27)

	radio_end.forEach(function(radio, i, radio_end) {	// в цикле заполняем словарь
  		end.set(radio.value, i);
	});

  	var rezault = false;

  	switch (command) {
  	case "begin_id": 						// получение id времени "с" по значению
    	rezault = begin.get(radio_time);
    	break;
  	case "end_id": 							// получение id времени "до" по значению
    	rezault = end.get(radio_time);
    	break;
  	default:
    	rezault = false;
	}
	return rezault;
}

function get_value_by_id(value, command){	// функция получения id по значению

	radio_begin = document.getElementsByName("time_begin");
	radio_end = document.getElementsByName("time_end");

	var begin = new Map([]);	// создаём пустой словарь, где каждый эл-т = время: индекс (0 - 27)

	radio_begin.forEach(function(radio, i, radio_begin) {	// в цикле заполняем словарь
  		begin.set(String(i), radio.value);
	});

	var end = new Map([]);	// создаём пустой словарь, где каждый эл-т = время: индекс (0 - 27)

	radio_end.forEach(function(radio, i, radio_end) {	// в цикле заполняем словарь
  		end.set(String(i), radio.value);
	});

  	var rezault = false;

  	switch (command) {
  	case "begin_value": 						// получение id времени "с" по значению
    	rezault = begin.get(value);
    	break;
  	case "end_value": 							// получение id времени "до" по значению
    	rezault = end.get(value);
    	break;
  	default:
    	rezault = false;
	}
	return rezault;
}

class Month{		
	constructor(month, name){
		this.month = document.getElementById(month);
		this.name = document.getElementById(name);
	}
	hiden(){	// скрыть месяц
		this.month.className = 'row d-none';
		this.name.style.display = 'none';
	}
	show(){		// показать месяц
		this.month.className = 'row d-block';
		this.name.style.display = 'block';
	}
}

class ButtonsTurn{		// кнопки "<" и ">"
	constructor(){
		this.left = document.getElementById("btn_left");
		this.right = document.getElementById("btn_right");
	}
	situation(count){	// состояние кнопок

		switch(count){
			case 0: 						// только правая вкл
				this.left.disabled = true;
				this.right.disabled = false;
			break;
			case 1: 						// обе вкл
				this.left.disabled = false;
				this.right.disabled = false;
			break;
			case 2: 						// только левая вкл
				this.left.disabled = false;
				this.right.disabled = true;
			break;
			default: 						// по дефолту только правая вкл
				this.left.disabled = true;
				this.right.disabled = false;
		}
	}
}

class TimePanel{
	constructor(tp_element){
		this.begin = document.getElementById(tp_element.begin)			// панель времени "с"
		this.end = document.getElementById(tp_element.end)				// панель времени "до"

		this.radio_begin = document.getElementsByName("time_begin");	// список radiobutton времени "с"  (из forms)
		this.radio_end = document.getElementsByName("time_end");		// список radiobutton времени "до" (из forms)

		this.tb = tp_element.tb;					// 
		this.te = tp_element.te;					// 
		this.begin_label = tp_element.lbegin;		// 
		this.end_label = tp_element.lend;			//
		// мобильная часть //
		this.mobile_begin = document.getElementById(tp_element.mobile_begin);
		this.mobile_end = document.getElementById(tp_element.mobile_end);
		this.m_select_begin = document.getElementsByName(tp_element.m_select_begin)[0];
		this.m_select_end = document.getElementsByName(tp_element.m_select_end)[0];
		this.mtb = tp_element.mtb;
		this.mte = tp_element.mte;
	}
	set_TimeBegin(value){
		this.begin.value = value;
		this.m_select_begin.value = get_id_by_value(value, "begin_id");
	}
	turn_begin(){	// показать время "с", время "до" скрыть
		this.begin.className = 'time_panel';
		this.end.className = 'd-none';


	}
	turn_end(){		// показать время "до", время "с" скрыть
		this.begin.className = 'd-none';
		this.end.className = 'time_panel';

	}
	begin_block(){	// перевод панели в состояние "не выбран день"
		for( var i=0; i<=27; i++)			
		{
			document.getElementById(this.begin_label + i).style = "cursor: default;";	// курсор стрелочка у begin_label
			document.getElementById(this.tb+ i).style = "background: #9d9d9d;";			// radio времени "с" делаем серым		
		}

		for(var i =0; i < this.radio_begin.length; i++)
		{
			this.radio_begin[i].checked = false;		// снимаем выбранный radio
			this.radio_begin[i].disabled = true;		// делаем его некликабельным
		}
	}
	begin_unblock(){
		for(var i =0; i <= 27; i++)
		{
			this.radio_begin[i].checked = false;		// снимаем выбранный radio
			this.radio_end[i].checked = false;			// снимаем выбранный radio

			if(color_time[i] == 'green'){				// если радио зеленый
				this.radio_begin[i].disabled = false;	// делаем его кликабельным
				this.radio_end[i].disabled = false;	// делаем его кликабельным
			}
			else{										// если красный
				this.radio_begin[i].disabled = true;	// делаем его НЕ кликабельным
				this.radio_end[i].disabled = true;	// делаем его НЕ кликабельным
			}
		}
		for( var i=0; i<=27; i++)				// окрашиваем radio
		{
			if(color_time[i] == 'green')
			{

				document.getElementById(this.tb + i).style = "background: #00dd78; cursor: pointer;";		// radio "с" делаем зеленым
				document.getElementById(this.te + i).style = "background: #00dd78; cursor: pointer;";		// radio "до" делаем зеленым
			}
			else{
				document.getElementById(this.tb + i).style = "background: red;";		// radio "с" делаем красным
				document.getElementById(this.te + i).style = "background: red;";		// radio "до" делаем красным
			}
		}


		this.mobile_begin.className = "mobile_time";
		this.m_select_begin.value = '';
		for( var i=0; i<=27; i++){
			if(color_time[i] == 'green'){
				document.getElementById(this.mtb+i).style="display: block;";
			}
			else{
				document.getElementById(this.mtb+i).style="display: none;"; 
			}
		}
	}
	begin_paint(){	// окрашиваем выбранное время в черный
		for( var i=0; i<=27; i++)			
		{
			var time =  document.getElementById(this.tb + i);
			if((i < time_begin_id) || (i > time_end_id))
			{
				if(color_time[i] == 'green')
				{
					time.style = "background: #00dd78; cursor: pointer;"
				}
				else{
					time.style = "background: red;"
				}
			}
			else
			{
				time.style = "background: black; cursor: pointer;"
			}
		}
	}
	mouse_paint(this_id){	// функция перерисовки по курсору

		if ( this_id >= time_begin_id)	// если курсор дальше времени "с"
		{	
			for( var i=0; i<=27; i++)
			{
				var time =  document.getElementById(this.te + i);
				if((i < time_begin_id) || (i > this_id )){		// всё, что за пределами выбранной области
					if(color_time[i] == 'green'){				// если радио зеленый
						time.style = "background: #00dd78; cursor: pointer;"
					}
					else{
						time.style = "background: red;"
					}
				}
				else{		// всё, что в пределах выбранной области
					if(color_time[i] == 'green' ){				// если радио зеленый
						if(i <= red_border.up){		// если не заходит за красную границу
							time.style = "background: black; cursor: pointer;"	// красим в черный
							this.radio_end[i].disabled = false;		// кликабельно
						}
						else{		// если заходит за красную границу
							this.radio_end[i].disabled = true;		// не кликабельно
						}
					}
					else{
						if(i < red_border.up)
						{
							red_border.up = i;
						}
					}
				}
			}
		}
		else 	// если курсор ниже времени "с"
		{
			for( var i=27; i>=0; i--)
			{
				var time =  document.getElementById(this.te + i);
				if((i > time_begin_id) || (i < this_id )){	// всё, что за пределами выбранной области
					if(color_time[i] == 'green'){				// если радио зеленый
						time.style = "background: #00dd78; cursor: pointer;"
					}
					else{
						time.style = "background: red;"
					}
				}
				else{	// всё, что в пределах выбранной области
					if(color_time[i] == 'green'){				// если радио зеленый
						if(i >= red_border.down){
							time.style = "background: black; cursor: pointer;"
							this.radio_end[i].disabled = false;		// кликабельно
						}
						else{
							this.radio_end[i].disabled = true;		// Не кликабельно
						}
					}
					else{	// если радио красный
						if(i > red_border.down)
						{
							red_border.down = i;
						}
					}
				}
			}
		}
	}
	black_radio_end(id){
		for(var i = 0; i <= 27; i++){
			if(i == id){
				document.getElementById(this.te + i).style= "background: black;";	// время "с" в черный
			}
			else{
				if(color_time[i] == 'green'){
					document.getElementById(this.te + i).style= "background: #00dd78;";	// в зеленый
				}
				else{
					document.getElementById(this.te + i).style= "background: red;";	// в зеленый
				}
				
			}
		}
	}
}

function turn_month(count){	// функция переключения месяца 
 
	let month_1 = new Month("mont1", "name_month1");
	let month_2 = new Month("mont2", "name_month2");
	let month_3 = new Month("mont3", "name_month3");

	switch (count) {
  	case 0:
  		month_1.show(); month_2.hiden(); month_3.hiden();	// показать 1-ый месяц
    break;
  	case 1:
  		month_1.hiden(); month_2.show(); month_3.hiden();	// показать 2-ой месяц
    break;
  	case 2:
  		month_1.hiden(); month_2.hiden(); month_3.show();	// показать 3-ий месяц
    break;
  	default:
    	month_1.show(); month_2.hiden(); month_3.hiden();	// по дефолту 1-ый месяц
	}
}

function turn_click(button_name){		// Функция обработки нажатия одной из кнопок "< или >"
	
	if (button_name == 'right'){		// если нажата ">" - прибавляем счетчик
		month_count++;		
	}
	else if (button_name == 'left'){	// если нажата "<" - убавляем счетчик
		month_count--;		
	}
	let buttons = new ButtonsTurn();	// объявляем кнопки
	buttons.situation(month_count);		// регулируем положение кнопок вкл/выкл
	turn_month(month_count);			// переключаем месяц
}


function select_room(select) {		// переключение комнаты
	document.getElementById("select_time").style = "display: none";
	var label_day = document.getElementsByName("day_room_" + select.value);		// получаем все дни данной комнаты
	for(var i =0; i < label_day.length; i++)
	{
		label_day[i].style = "border: 1px solid #d1d1d1;";		// дефолтная рамка у всех дней
	}

	for (var i = 0; i < 3; i++){
		for (var j = 0; j < select.length; j++){
			var room = document.getElementById("month" + i + "_room" + j);
			if (select.value == select[j].value){
				
				room.className = 'calendar';		// месяцы данной комнаты сделать видимыми
			} 
			else{
				room.className = 'd-none';		// месяцы других комнат скрыть
			}
		}
	}

	let time_panel = new TimePanel(tp_element);										// объявить временную панель
	time_panel.turn_begin();														// показать время "с", время "до" скрыть
	time_panel.begin_block();														// сделать панель "с" недоступной для нажатия

	document.getElementById("button_reservation").style.display = 'none';			// кнопка "забронировать" выкл
	this_select_room = select.value; 												// запомнить выбранную комнату
}

function SwapTime(){	// функция замены местами time_begin_id и time_end_id

	var swap = time_begin_id
  	time_begin_id = time_end_id
  	time_end_id = swap

  	document.getElementsByName('time_begin')[time_begin_id].checked = true;
  	document.getElementsByName('time_end')[time_end_id].checked = true;
}

function change_time_begin(radio_time_begin) {		// функция изменения времени "с"

	let time_panel = new TimePanel(tp_element);									// объявить временную панель
	time_panel.turn_end();														// показать время "до", время "с" скрыть

  	time_begin_id = get_id_by_value(radio_time_begin.value, "begin_id");		// записать выбранное время "с"

  	document.getElementById("button_reservation").style.display = 'none';		// кнопка "забронировать" выкл
  	red_border.up = 27;
	red_border.down = 0;	// сбрасываем красную границу	

	time_panel.black_radio_end(time_begin_id);

	time_panel.set_TimeBegin(radio_time_begin.value);
}

function change_time_end(radio_time_end) {		// функция изменения времени "до"

	let time_panel = new TimePanel(tp_element);									// объявить временную панель
	time_panel.turn_begin();													// показать время "c", время "до" скрыть

  	time_end_id = get_id_by_value(radio_time_end.value, "end_id");				// записать выбранное время "до"

  	if (time_end_id < time_begin_id )	// если время "с" больше чем время "до"
  	{
  		SwapTime();						// меняем местами их значения
  	}
	time_panel.begin_paint();			// окрашиваем время "с" в зеленый и черный

	document.getElementById("button_reservation").style.display = 'block';		// кнопка "забронировать" вкл
}


function mouse_time_end(id_time) {		// отслеживание курсора на временной панеле
	this_id = parseInt(id_time, 10)						// текущий id
	let time_panel = new TimePanel(tp_element);			// объявить временную панель
	time_panel.mouse_paint(this_id);					// функция перерисовки
}

function color_reservation_times(this_select_day){		// функция получения списка цветов временной панели
	for(var i=0; i < window.rooms.length; i++){
		if(window.rooms[i].number == this_select_room){
			for(var j=0; j < window.rooms[i].list_day.length; j++){
				if(window.rooms[i].list_day[j].date == this_select_day){
					return(window.rooms[i].list_day[j].list_time);
				}
			}
		}
	}
}

function change_day(radio_day) {						// Функция выбора дня

	document.location.href = "#select_time";			// переход по ссылке 
	document.getElementById("select_time").style = "display: block";

	var select_room_id = document.getElementById("room_selector");
	var label_day = document.getElementsByName("day_room_" + select_room_id.value);
	for(var i =0; i < label_day.length; i++)
	{
		if(label_day[i].id == ('day_' + radio_day.value))
		{
			label_day[i].style = "border: calc(0.1em + 0.2vw) solid black;";	// делаем рамку у выбранного дня	
		}
		else
		{
			label_day[i].style = "border: 1px solid #d1d1d1;";
		}
	}

	var this_select_day = radio_day.value;										// выбранный день
	color_time = color_reservation_times(this_select_day);						// получить список цветов временнйо панели
	
	let time_panel = new TimePanel(tp_element);									// объявить временную панель
	time_panel.turn_begin();													// показать время "c", время "до" скрыть
	time_panel.begin_unblock();													// разблокировать панель времени "с"

	time_begin_id = false;					// обнуляем
	time_end_id = false;					//	переменные

	let mobile_panel = new MobilePanel(mt_element);			// объявляем мобильную панель времени
	mobile_panel.begin_unblock();							// разблочим время "с"
	mobile_panel.end_block();								// блочим время "до"

	document.getElementById("button_reservation").style.display = 'none';		// кнопка "забронировать" выкл
}


function mobile_change_TimeBegin(select){
	var radio_begin = document.getElementsByName("time_begin")[0];
	radio_begin.value =get_value_by_id(select.value, "begin_value");
	change_time_begin(radio_begin);
}