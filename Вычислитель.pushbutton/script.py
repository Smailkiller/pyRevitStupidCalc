# coding: utf-8
import clr
import os

clr.AddReference('PresentationFramework')
clr.AddReference('WindowsBase')
clr.AddReference('PresentationCore')

import System
from System.Windows import Window, Thickness, VerticalAlignment, HorizontalAlignment
from System.Windows.Controls import Grid, Button, TextBox, ListBox, StackPanel, Label, Orientation
from System.Windows.Media import Brushes, FontFamily
from System.Windows.Input import TextCompositionEventArgs, KeyEventArgs, Key

class CalculatorWindow(Window):
    def __init__(self):
        self.Title = u"Расширенный калькулятор для модели"
        self.Width = 600
        self.Height = 450
        self.Background = Brushes.WhiteSmoke

        # Основной грид с двумя колонками
        self.grid = Grid()
        self.Content = self.grid

        # Создаем 2 колонки: калькулятор (40%), история (60%)
        col1 = System.Windows.Controls.ColumnDefinition()
        col1.Width = System.Windows.GridLength(2, System.Windows.GridUnitType.Star)
        col2 = System.Windows.Controls.ColumnDefinition()
        col2.Width = System.Windows.GridLength(3, System.Windows.GridUnitType.Star)
        self.grid.ColumnDefinitions.Add(col1)
        self.grid.ColumnDefinitions.Add(col2)

        # === Левая часть: калькулятор ===
        self.calc_grid = Grid()
        System.Windows.Controls.Grid.SetColumn(self.calc_grid, 0)
        self.grid.Children.Add(self.calc_grid)

        # Строки для калькулятора: 1 под дисплей + 5 под кнопки
        for i in range(6):
            self.calc_grid.RowDefinitions.Add(System.Windows.Controls.RowDefinition())
        # 4 колонки для кнопок
        for i in range(4):
            self.calc_grid.ColumnDefinitions.Add(System.Windows.Controls.ColumnDefinition())

        # Поле ввода / дисплей
        self.display = TextBox()
        self.display.Margin = Thickness(10)
        self.display.FontSize = 28
        self.display.FontFamily = FontFamily("Segoe UI")
        self.display.IsReadOnly = False
        self.display.VerticalContentAlignment = VerticalAlignment.Center
        self.display.Text = ""
        System.Windows.Controls.Grid.SetRow(self.display, 0)
        System.Windows.Controls.Grid.SetColumnSpan(self.display, 4)
        self.calc_grid.Children.Add(self.display)

        # Ограничение ввода символов
        self.display.PreviewTextInput += self.on_text_input
        self.display.PreviewKeyDown += self.on_preview_key_down

        # Кнопки
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3),
        ]

        for (content, row, col) in buttons:
            btn = Button()
            btn.Content = content
            btn.FontSize = 20
            btn.Margin = Thickness(5)
            btn.Click += self.on_button_click
            System.Windows.Controls.Grid.SetRow(btn, row)
            System.Windows.Controls.Grid.SetColumn(btn, col)
            self.calc_grid.Children.Add(btn)

        equals_btn = Button()
        equals_btn.Content = "="
        equals_btn.FontSize = 20
        equals_btn.Margin = Thickness(5)
        equals_btn.Click += self.on_equals_click
        System.Windows.Controls.Grid.SetRow(equals_btn, 5)
        System.Windows.Controls.Grid.SetColumn(equals_btn, 0)
        System.Windows.Controls.Grid.SetColumnSpan(equals_btn, 4)
        self.calc_grid.Children.Add(equals_btn)

        # === Правая часть: история с фиксированной высотой и заголовком ===
        self.history_panel = StackPanel()
        self.history_panel.Margin = Thickness(10)
        self.history_panel.Orientation = Orientation.Vertical
        System.Windows.Controls.Grid.SetColumn(self.history_panel, 1)
        self.grid.Children.Add(self.history_panel)

        self.history_label = Label()
        self.history_label.Content = u"История"
        self.history_label.FontSize = 16
        self.history_label.FontFamily = FontFamily("Segoe UI")
        self.history_panel.Children.Add(self.history_label)

        self.history_list = ListBox()
        self.history_list.Height = 220  # ограничиваем высоту истории
        self.history_list.FontSize = 14
        self.history_list.FontFamily = FontFamily("Segoe UI")
        self.history_panel.Children.Add(self.history_list)

        self.history = []  # список строк истории

    def on_text_input(self, sender, e):
        allowed_chars = '0123456789+-/*.'
        for ch in e.Text:
            if ch not in allowed_chars:
                e.Handled = True  # запретить ввод
                break

    def on_preview_key_down(self, sender, e):
        allowed_keys = [Key.Back, Key.Delete, Key.Left, Key.Right, Key.Tab]
        if e.Key not in allowed_keys:
            pass

    def on_button_click(self, sender, event):
        val = sender.Content
        if val == 'C':
            self.display.Text = ""
            self.display.CaretIndex = 0
        else:
            caret_index = self.display.CaretIndex
            text = self.display.Text
            self.display.Text = text[:caret_index] + val + text[caret_index:]
            self.display.CaretIndex = caret_index + 1

    def on_equals_click(self, sender, event):
        expr = self.display.Text
        try:
            result = eval(expr)
            result_str = str(result)
            self.display.Text = result_str
            self.display.CaretIndex = len(result_str)

            # Добавляем в историю
            hist_entry = "{} = {}".format(expr, result_str)
            self.history.append(hist_entry)

            # Обновляем ListBox истории
            self.history_list.Items.Clear()
            # Показываем последние 20 записей
            for entry in self.history[-20:]:
                self.history_list.Items.Add(entry)

            # Прокрутка вниз к последнему элементу
            if self.history_list.Items.Count > 0:
                self.history_list.ScrollIntoView(self.history_list.Items[self.history_list.Items.Count - 1])

        except:
            self.display.Text = u"Ошибка"
            self.display.CaretIndex = len(self.display.Text)


def run():
    win = CalculatorWindow()
    win.ShowDialog()


if __name__ == "__main__":
    run()
