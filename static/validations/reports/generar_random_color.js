export const generateRandomRGBColor = () => {
    const randomNumber = (min , max) => {
        return Math.floor(Math.random() * (max - min + 1) ) + min;
    }   
    const color = `rgb(${randomNumber(0,255)}, ${randomNumber(0,255)}, ${randomNumber(0,255)})`;
    return color;
}

export const generateRandomRGBColorList = (data) => {
    let colorList = [];
    for(let i=0; i < data.length; i++){
        colorList.push(generateRandomRGBColor())
    }
    return colorList;
}

export const listOfColors = () => [
    "rgb(255,0,0)", //red
    "rgb(255,255,0)", //blue
    "rgb(255,99,71)", //tomato
    "rgb(255,255,0)", //yellow
    "rgb(0,255,0)", //lime
    "rgb(32,178,170)", //light sea
    "rgb(138,43,226)", //blue violet
    "rgb(210,105,30)", //chocolate
    "rgb(255,222,173)", //navajo white
    "rgb(128,128,128)", //gray
    "rgb(60,179,113)", //medium sea green
    "rgb(0,255,255)", //aqua
    "rgb(0,128,0)", //green
    "rgb(255,105,180)", //hot pink
    "rgb(160,82,45)", //sienna
    "rgb(65,105,225)", //royal blue
]

export const beautyRGBColorList = (data) => {
    let colorList = [];
    for(let i=0; i < data.length; i++){
        colorList.push(listOfColors()[i])
    }
    return colorList;
}

