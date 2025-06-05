// Kakao Maps API가 로드된 후에 실행될 코드
kakao.maps.load(function() {
    var container = document.getElementById('map'); // 지도를 표시할 div
    var options = {
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표 (기본값: 카카오 본사)
        level: 3 // 지도의 확대 레벨
    };

    // 지도 생성
    var map = new kakao.maps.Map(container, options);

    // 현재 위치로 이동 버튼 클릭 이벤트
    var currentLocationBtn = document.getElementById('current-location-btn');
    currentLocationBtn.addEventListener('click', function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat = position.coords.latitude; // 위도
                var lon = position.coords.longitude; // 경도
                var locPosition = new kakao.maps.LatLng(lat, lon); // 현재 위치를 담을 LatLng 객체

                // 지도 중심을 현재 위치로 이동
                map.setCenter(locPosition);

                // 현재 위치에 마커 표시 (선택 사항)
                var marker = new kakao.maps.Marker({
                    map: map,
                    position: locPosition
                });

                // 정보 창 표시 (선택 사항)
                var iwContent = '<div style="padding:5px;">현재 위치</div>', // 인포윈도우에 표출될 내용으로 HTML 문자열이나 DOM Element 입니다
                    iwRemoveable = true;

                var infowindow = new kakao.maps.InfoWindow({
                    content : iwContent,
                    removable : iwRemoveable
                });
                infowindow.open(map, marker);

            }, function(error) {
                // 위치 정보를 가져오는 데 실패했을 때
                alert('현재 위치를 가져올 수 없습니다. 위치 권한을 확인해주세요.');
                console.error(error);
            }, {
                enableHighAccuracy: true, // 높은 정확도 요구
                timeout: 5000,           // 5초 이내 응답
                maximumAge: 0            // 캐시된 위치 정보 사용 안 함
            });
        } else {
            alert('이 브라우저는 Geolocation을 지원하지 않습니다.');
        }
    });

    // 예시: 특정 장소에 마커 추가 (Paju-si, Gyeonggi-do)
    var pajuPosition = new kakao.maps.LatLng(37.750275, 126.902998); // 파주시청 근처 좌표
    var pajuMarker = new kakao.maps.Marker({
        position: pajuPosition,
        map: map
    });

    var pajuInfoWindow = new kakao.maps.InfoWindow({
        content : '<div style="padding:5px;">파주시청</div>',
        removable : true
    });

    kakao.maps.event.addListener(pajuMarker, 'click', function() {
        pajuInfoWindow.open(map, pajuMarker);
    });

    // 지도 중심을 파주로 이동
    map.setCenter(pajuPosition);
});