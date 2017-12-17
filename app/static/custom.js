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
    var q_id = [];
    $("input[name^=q]").each(function(i){
        q_id[i] = $(this).attr("name");
    });
    var data = [];
    $("tr.output").each(function(i){
        var input_data = new Object();
        $(this).children().each(function(j){
            if (j < q_id.length){
                input_data[q_id[j]] = $(this).text();
            }
        });
        data[i] = input_data;
    });
    $.post($("form").attr("action"), data, function(){
        alert("提交成功");
    });
    $("tr.output").remove();
}