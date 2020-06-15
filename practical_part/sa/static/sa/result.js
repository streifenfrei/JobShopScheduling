$(document).ready(function(){

    $("#result_table_select").change(function(){
        
        var table_id = $("#result_table_select").val();
       
        $.ajax({
            type: "GET",
            async: true,
            url:"/results/" + table_id,
            data: {
                'table_id' : table_id, 
            },
            success: function(res) {
                $('#result_table').html(res.content);
            
            },
            error: function () {
                alert("error");
            }
        });
    })

    $("#schedule_close").click(function(){
        
        card = document.getElementById('image_schedule')
        card.style.display = "none"
    
    })

    
})

function show_schedule(id){

    $.ajax({
        type: "GET",
        async: true,
        url:"/results/" + id + "/show",
        data: {
            'table_id' : id, 
        },
        success: function(res) {
            s = document.getElementById('schedule_plt')
            s.src = res.source
            card = document.getElementById('image_schedule')
            card.style.display = "block"

        },
        error: function () {
            alert("error");
        }
    })
}