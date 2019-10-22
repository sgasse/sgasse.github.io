function setBackground(month) {
    bgLayer = document.getElementById('background');
    switch (month) {
        case 11:
        case 12:
        case 1:
        case 2:
        case 3:
            bgLayer.style.backgroundImage = 'url(img/bg_ice_small.jpg)';
            break;
        case 4:
        case 5:
            bgLayer.style.backgroundImage = 'url(img/bg_lawn_small.jpg)';
            break;
        case 6:
        case 7:
        case 8:
            bgLayer.style.backgroundImage = 'url(img/bg_sea_small.jpg)';
            break;
        case 9:
        case 10:
            bgLayer.style.backgroundImage = 'url(img/bg_field_small.jpg)';
            break;
    }
}

var today = new Date;
month = today.getMonth() + 1; // January is 0 internally
setBackground(month);