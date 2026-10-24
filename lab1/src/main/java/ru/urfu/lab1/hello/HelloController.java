package ru.urfu.lab1.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.HashMap;

@RestController
public class HelloController {

    private ArrayList<String> arrayList;
    private HashMap<Integer, String> hashMap;

    @GetMapping("/hello")
    public String hello(@RequestParam(value = "name",
            defaultValue = "World") String name) {
        return String.format("Hello %s!", name);
    }

    // При первом вызове создаётся пустой ArrayList, при последующих - в него добавляется значение
    @GetMapping("/update-array")
    public String updateArrayList(@RequestParam(value = "s") String s) {
        if (arrayList == null) {
            arrayList = new ArrayList<>();
            return "Создан пустой ArrayList";
        }
        arrayList.add(s);
        return String.format("В ArrayList добавлено значение: %s", s);
    }

    @GetMapping("/show-array")
    public ArrayList<String> showArrayList() {
        return arrayList == null ? new ArrayList<>() : arrayList;
    }

    // При первом вызове создаётся пустой HashMap, при последующих - в него добавляется значение
    @GetMapping("/update-map")
    public String updateHashMap(@RequestParam(value = "s") String s) {
        if (hashMap == null) {
            hashMap = new HashMap<>();
            return "Создан пустой HashMap";
        }
        int key = hashMap.size() + 1;
        hashMap.put(key, s);
        return String.format("В HashMap добавлено значение: %d=%s", key, s);
    }

    @GetMapping("/show-map")
    public HashMap<Integer, String> showHashMap() {
        return hashMap == null ? new HashMap<>() : hashMap;
    }

    @GetMapping("/show-all-lenght")
    public String showAllLenght() {
        int arraySize = arrayList == null ? 0 : arrayList.size();
        int mapSize = hashMap == null ? 0 : hashMap.size();
        return String.format("Количество элементов в ArrayList: %d, количество элементов в HashMap: %d",
                arraySize, mapSize);
    }
}
