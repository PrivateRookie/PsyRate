$(document).on("click", "button.remove", function(){
   delete_();
   $(this).parents("tr").remove();
});
$(document).on("click", "button.edit", edit);
$(document).on("click", "button.add", add);
$(document).on("click", "button.sub", function(){});
$(document).ready(preload);

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
 
function add(){
    submit_();
}
 
 function edit(){
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
 
function delete_(){
    $.ajax({
        type:'get',
        url:baseurl + 'delete/' + $("tr.input").attr("current-id")
    });
}

function preload(){
    $.ajax({
        type:'post',
        url:baseurl + 'preload/',
        data:$("input[name='form_name']").serialize(),
        success:function(data){
            for (i = 0; i < data["records"].length; i++){
                $("table tr:last").after("<tr class='output'></tr>");
                for (j = 0; j < data["records"][i].length; j++){
                    $("table tr:last").append("<td>" + data["records"][i][j] + "</td>");
                }
               $("table tr:last").append("<td><button class='remove btn btn-warning' type='button'><span class='remove glyphicon glyphicon-minus'></span></button></td>");
               $("table tr:last").append("<td><button class='edit btn btn-primary' type='button'><span class='remove glyphicon glyphicon-pencil'></span></button></td>");
            }
        }
    });
}