
$(document).ready(function(){

    $("#slected_table").change(function(){
        
        var id = $("#slected_table").val();
       
        $.ajax({
            type: "GET",
            async: true,
            url:"/test/" + id,
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
        var temp = $("#temp").val();
        var r_rate = $('#rate').val();
        var count = $('#count').val();
        var ci = $('#count_i').val();
        var sa = $('#sa_num').val();
        var btng = document.getElementById('rsa')
        btng.style.backgroundColor = "Indigo"
       
        $.ajax({
            type: "GET",
            async: true,
            url:"/test/" + id + "/" + temp +"/" + r_rate + "/" + count + "/" + ci + "/" + sa + "/execute",
            data: {
                'Id' : id, 
            },
            success: function(res) {
                btng.style.backgroundColor = "Blue"
                if (res.success = 1){
                    s = document.getElementById('new_schedule')
                    s.src = res.source
                    l = document.getElementById('time')
                    l.innerHTML = res.result_length
                    rt = document.getElementById('runtime')
                    rt.innerHTML = res.runtime
                    card = document.getElementById('new_image_schedule')
                    card.style.display = "block"
                }
                else{
                    alert("New Result is not in the top ten")
                }
            },
            error: function () {
                alert("Sa failed");
                btng.style.backgroundColor = "Blue"
            }
        });
    })

    $("#rsa_f").click(function(){
        
        var btng = document.getElementById('rsa_f')
        var id = $("#slected_table").val();
        btng.style.backgroundColor = "Indigo"
       
        $.ajax({
            type: "GET",
            async: true,
            url:"/run/" + id + "/sa",
            data: {
                'Id' : id, 
            },
            success: function(res) {
                btng.style.backgroundColor = "Blue"
                if (res.success = 1){
                    s = document.getElementById('new_schedule')
                    s.src = res.source
                    l = document.getElementById('time')
                    l.innerHTML = res.result_length
                    rt = document.getElementById('runtime')
                    rt.innerHTML = res.runtime
                    card = document.getElementById('new_image_schedule')
                    card.style.display = "block"
                }
                else{
                    alert("New Result is not in the top ten")
                }
            },
            error: function () {
                alert("Sa failed");
                btng.style.backgroundColor = "Blue"
            }
        });
    })

    $("#new_schedule_close").click(function(){
        
        card = document.getElementById('new_image_schedule')
        card.style.display = "none"
    
    })
})
