
$(document).ready(function(){

    $("#slected_table").change(function(){
        
        var id = $("#slected_table").val();
       
        $.ajax({
            type: "GET",
            async: true,
            url:"/run/" + id,
            data: {
                'Id' : id, 
            },
            success: function(res) {
                $('#render_table').html(res.content);
            
            },
            error: function () {
                alert("error");
            }
        });
    })

    $("#rsa").click(function(){
        
        var id = $("#slected_table").val();
       
        $.ajax({
            type: "GET",
            async: true,
            url:"/run/" + id + "/execute",
            data: {
                'Id' : id, 
            },
            success: function(res) {
                alert(res)
            },
            error: function () {
                alert("erro_erer");
            }
        });
    })
})
