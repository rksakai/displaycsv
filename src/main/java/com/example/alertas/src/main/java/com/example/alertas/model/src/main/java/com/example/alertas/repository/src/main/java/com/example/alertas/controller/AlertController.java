package com.example.alertas.controller;

import com.example.alertas.model.Alert;
import com.example.alertas.repository.AlertRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class AlertController {

    private final AlertRepository repository;

    public AlertController(AlertRepository repository) {
        this.repository = repository;
    }

    // Página inicial — lista de alertas
    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("alerts", repository.findAll());
        return "index";
    }

    // Formulário de novo alerta
    @GetMapping("/new")
    public String form() {
        return "new";
    }

    // Recebe o POST do formulário
    @PostMapping("/new")
    public String create(
        @RequestParam String descricao,
        @RequestParam String categoria,
        @RequestParam double latitude,
        @RequestParam double longitude,
        Model model
    ) {
        Alert alert = new Alert(descricao, categoria, latitude, longitude, "Pendente");
        repository.save(alert);
        return "redirect:/";
    }
}
