$(document).on("click", "button.remove", function(){
   $.ajax({
        type:'get',
        data:$("input[name='form_name']").serialize(),
        url:baseurl + 'delete/' + $(this).parents("tr").attr("current-id")
    });
   $(this).parents("tr").remove();
});
$(document).on("click", "button.edit", edit_);
$(document).on("click", "button.add", add_);
$(document).on("click", "button.sub", function(){
    alert("提交成功");
});
$(document).ready(preload_);

var baseurl = "http://localhost:5000/ajax/";
 
function set_current_id(id){
    var input = [];
    $(".form-control").each(function(i){
        if ($(this).is("input")){
           input[i] = $(this).val();
        }
        else if ($(this).is("select")){
            input[i] = $(this).find("option:selected").text();
        }
        $(this).val(null);
    });
    $("table tr:last").after("<tr class='output'></tr>");
    for (i = 0; i < input.length; i++){
        $("table tr:last").append("<td>" + input[i] + "</td>");
    }
    $("table tr:last").append("<td><button class='remove btn btn-warning' type='button'><span class='remove glyphicon glyphicon-minus'></span></button></td>");
    $("table tr:last").append("<td><button class='edit btn btn-primary' type='button'><span class='remove glyphicon glyphicon-pencil'></span></button></td>");
    $("table tr:last").attr("current-id", id);
    $("tr.input").attr("current-id", 0);
}
 
function add_(){
    submit_();
}
 
 function edit_(){
    if ($("tr.input").attr("current-id") != 0){
        alert("请先提交工作区的记录然后再点击修改。");
        return
    }
    $("tr.input").attr("current-id", $(this).parents("tr").attr("current-id"));
    var values = [];
    $(this).parents("tr").children().each(function(i){
        values[i] = $(this).text();
    });
    values.pop();
    values.pop();
    $(".form-control").each(function(i){
        if ($(this).is("input")){
            $(this).val(values[i]);
        }
        else{
            $(this).val(values[i]);
            $(this).children().each(function(j){
                if ($(this).text() == values[i]){
                    $(this).attr("selected", true);
                }
                else{
                    $(this).attr("selected", false); 
                }
            });
        }
    });
    $(this).parents("tr").remove();
    
 }
 
 function submit_(){
    $.ajax({
       type:'post',
       url:baseurl + $("tr.input").attr("current-id"),
       data:$("form").serialize(),
       cache:false,
       success:set_current_id
    })
 }

function preload_(){
    $.ajax({
        type:'post',
        url:baseurl + 'preload/',
        data:$("input[name='form_name'], input[name='status']").serialize(),
        success:function(data){
            var data = JSON.parse(data);
            for (i = 0; i < data.records.length; i++){
                $("table tr:last").after("<tr class='output'></tr>");
                $("table tr:last").attr("current-id", data.records[i].id);
                $(".form-control").each(function(j){
                    if ($(this).is("input")){
                        $("table tr:last").append("<td>" + data.records[i].questions[j] + "</td>");
                    }
                    else{
                        $(this).children("option").each(function(k){
                            if ($(this).val() == data.records[i].questions[j]){
                                $("table tr:last").append("<td>" + $(this).text() + "</td>");
                            }
                        });
                    }
                });
               $("table tr:last").append("<td><button class='remove btn btn-warning' type='button'><span class='remove glyphicon glyphicon-minus'></span></button></td>");
               $("table tr:last").append("<td><button class='edit btn btn-primary' type='button'><span class='remove glyphicon glyphicon-pencil'></span></button></td>");
            }
        }
    });
}