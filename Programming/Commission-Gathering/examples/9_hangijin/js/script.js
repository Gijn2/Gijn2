$(function(){
    var total = 0; // 초기 총 가격을 0으로 설정합니다.

    $('#btn').click(function(){
        alert("안녕");
    });
    
    $("select").change(function(){
        if($(this).val() != 0){
            var tr = $('<tr/>');
            tr.append("<td>"+$(this).siblings('#label').text()+"</td>");
            tr.append("<td>"+$(this).siblings('span[id^="price"]').text()+"</td>");
            tr.append("<td>"+$(this).val()+"</td>");
            tr.append("<td><input type='button' value='삭제' class='bDelete'></td>");
            $('#listtr').after(tr);

            // 입력된 음식 가격 띄우기
            var price = parseInt($(this).siblings('span[id^="price"]').text()); // 메뉴의 가격
            var count = parseInt($(this).val()); // 선택된 갯수
            total += price * count; // 총 가격에 추가합니다.

            // 총합을 #total 입력란에 표시
            $('#total').val(total);
        }
    });

    $('#listTable').on('click','.bDelete',function(){
        var price = parseInt($(this).closest('tr').find('td:eq(1)').text()); // 삭제되는 항목의 가격
        var count = parseInt($(this).closest('tr').find('td:eq(2)').text()); // 삭제되는 항목의 갯수
        total -= price * count; // 삭제되는 항목의 가격을 총 가격에서 제거합니다.
        $(this).closest('tr').remove();
        $('#total').val(total); // 변경된 총 가격을 업데이트합니다.
    });
    
    
    $('.bxslider').bxSlider({
	  minSlides: 1,
	  maxSlides: 3,
	  slideWidth: 960,
	  slideMargin: 10,
	  slidehight: 600,
	  ticker: true,
	  speed: 20000
	  
	});
	
});
