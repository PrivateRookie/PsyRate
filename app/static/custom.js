$(document).on("click", "button.remove", function(){
    $(this).parents("tr")
    $(this).parents("tr").remove();
});
$(document).on("click", "button.edit", edit);
$(document).on("click", "button.add", add);
$(document).on("click", "button.sub", submit_);


function add(){
    submit_($("tr.input").attr('current-id'));  
}

function edit(){
    var record_id = $(this).parents("tr").attr('record-id');
    var request_url = 'http://localhost:5000/test/' + record_id;
    var values = [];
    $(this).parents("tr").children().each(function(i){
        values[i] = $(this).text();
    });
    values.pop();
    values.pop();
    $("[name^=q]").each(function(i){
        if ($(this).is("input")) {
            $(this).val(values[i]);
        }
        else {
            $(this).children().each(function(j){
                if ($(this).text() == values[i]){
                    $(this).attr('selected', true);
                    console.log($(this).text());
                }
                else {
                    $(this).attr('selected', false);
                }
            });
        }
    });
    $("tr.input").attr('current-id', record_id);
    $(this).parents("tr").remove();
}

function success_fun(data, status, xhr){
    var input = [];
    $(".form-control").each(function(i){
        if ($(this).is('input')) {
            input[i] = $(this).val();
        }
        else {
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
    $("table tr:last").attr('record-id', data);
    $("tr.input").attr("current-id", 0);
}

function submit_(id){
    $.ajax({
        type:'post',
        url:'http://localhost:5000/test/' + String(id),
        data:$("form").serialize(),
        dataType:'text',
        success:success_fun,
        cache:false})
}