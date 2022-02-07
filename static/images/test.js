function laskecount() {
    count = names.length;
    return count;
}

function definename(num) {
    name = names[num];
    return name;
}

function definenumber(name) {
    for (i = 0; i < names.length; i++) {
        if (names[i] == name) {
            number = i;
            return number;

        }
        continue;
    }

}


return {
    count:laskecount,
    name: definename(),
    number: number
}
