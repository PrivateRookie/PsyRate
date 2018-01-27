$(document).on("click", "button.remove", function(){
    $(this).parents("tr").remove();
});
$(document).on("click", "button.edit", edit);
$(document).on("click", "button.add", add);
$(document).on("click", "button.sub", submit_);

function add(){
    var input = [];
    $(".form-control").each(function(i){
        input[i] = $(this).val();
        $(this).val(null);
    });
    $("table tr:last").after("<tr class='output'></tr>");
    for (i = 0; i < input.length; i++){
        $("table tr:last").append("<td>" + input[i] + "</td>");
    }
    $("table tr:last").append("<td><button class='remove btn btn-warning' type='button'><span class='remove glyphicon glyphicon-minus'></span></button></td>");
    $("table tr:last").append("<td><button class='edit btn btn-primary' type='button'><span class='remove glyphicon glyphicon-pencil'></span></button></td>");
    submit_();
}

function edit(){
    var values = [];
    $(this).parents("tr").children().each(function(i){
        values[i] = $(this).text();
    });
    values.pop();
    values.pop();
    $("input[name^=q]").each(function(i){
        $(this).val(values[i]);
    });
    $(this).parents("tr").remove();
}

function submit_(){
    $.ajax({
        type:'post',
        url:$("form").attr("action"),
        data:$("form").serialize(),
        cache:false,
    dataType:'json'})
}