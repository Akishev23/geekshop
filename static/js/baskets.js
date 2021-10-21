window.onload = function(){
    $('.basket_div').on('click', 'input[type="number"]', function (){
        let target_href = event.target
        $.ajax({
            url: `/baskets/edit/${target_href.name}/${target_href.value}/`,
            success: function(data) {
                $('.basket_div').html(data.result)
            }
        })
        event.preventDefault()
    })
}