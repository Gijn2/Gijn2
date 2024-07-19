<%@ page contentType="text/html; charset=UTF-8"%>
<?php
	$con=mysqli_connect("192.168.0.210","seoulinfo","seoul","seoulinfo") or dis("접속 실패");
	
	$sql="select * from evc";
	
	$ret=mysqli+query($con, $sql);
	
	$arr=array();

	while($row=mysqli_fetch_array($ret)){
		array_push($arr, [(double)$row['evc_lat'], (double)$row['evc_long'], $row['evc_name']]);
	}
	
	// arr 배열에 [위도, 경도, 충전소이름] 형태로 저장
	// echo var_dump($arr); // 배열 arr에 잘 들어갔는지 확인하기 위함
	
	mysqli_close($con);
	
?>
<%@ page contentType="text/html; charset=UTF-8"%>
<!DOCTYPE html>
<html>
	<head>
		<title>다중 마커, 다중 인포윈도우</title>
		<meta name="viewport" content="initial-scale=1.0, user-scalable=no">
		
		<style type="text/css">
			html {height : 100%}
			body {height : 100%; margin:0; padding:0;}
			h1	 {text-align: center;}
			#map {width:90%; height:80%; border:solid blue; margin-left:auto; margin-right:auto;}
		</style>
	</head>
		<script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=e4d5069dc9a490e0b400e0844235a47e&libraries=services"></script>
		<script type="text/javascript">
			window.onload = function(){
				var position = new kakao.maps.LatLng(37,126);
				var map = new kakao.maps.Map(document.getElementById('map'),{
					center:position
					,level:8
					,mapTypeId: kakao.maps.MapTypeId.ROADMAP });
				var zoomControl = new kakao.maps.ZoomControl();
				map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);
				var mapTypeControl = new kakao.maps.MapTypeControl();
				map.addControl(mapTypeControl, kakao.maps.ControlPosition.TOPRIGHT);
				
				var locations = <?php echo json_encode($arr); ?>;
				for(i=0; i < location; i++){
					var marker = new kakao.maps.Marker({
						position: new kakao.maps.LatLng(locations[i][0], locations[i][1])
					});
					marker.setMap(map);
					kakao.maps.event.addListener(marker, 'click', (function(marker, i){
						reutrn function(){
							var infowindow = new kakao.maps.infoWindow({
								content : '<p style="margin:7px 22px 7px 12px; font:12px;/1.5 sans-serif">' + locations[i][2] + '</p>'
								
								,removable : true
							});
							
							infoWindow.open(map, marker);}
						})
					(marker, i));
				}
			};
		</script>
	<body>
		<div id='map'></div>
	</body>
</html>
