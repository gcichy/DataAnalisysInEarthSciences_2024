# Analiza Danych w Naukach o Ziemi, Projekt 1 – Standardized Precipitation Index (SPI) 

Celem poniższego projektu jest wyliczenie miary SPI dla wybranego obszaru w Polsce na podstawie dobowych danych opadowych dostępnych na stronie: https://danepubliczne.imgw.pl.

Szczegółowe instrukcje i wytyczne dostępne są w pliku: docs/projekt1_instrukcja.pdf.

## Kroki, które należy wykonać w celu odtworzenia przeprowadzonej analizy:##
### 1. Otwarcie pliku src/main_script.py. ###

W tym pliku znajduje się funkcja main, po której wykonaniu użytkownik otrzyma wyniki analizy.

### 2. Uruchomienie pliku main_script.py ###

**2.1 Pobieranie plików.**
<br>
Ze względu na ilość plików proces ten potrwa do kilku minut.
<br><br>

**2.2 Łączenie plików w jeden DataFrame.**
<br>
Następnie program rozpocznie wczytywanie i łączenie kolejnych plików do jednego data frame'u, któy docelowo zapisany zostanie jako data/raw/merged_data.csv 
<br><br>

**2.3 Wyświetlenie mapy stacji** 
<br>
Ostatnim etapem wczytywania danych jest wyświetlenie mapy województwa Podkarpackiego z nałożonymi stacjami wykorzystanymi do obliczeń SPI.

Po zamknięciu wykresu program wznowi działanie.

### 3. EDA
<br>
W tym kroku wykonana została eksploracyjna analiza danych. W jej ramach uzupełniane/usuwane są wartości brakujące, występuje transformacja kolumn oraz wizualizacje danych. Wynikowy plik tego etapu programu zapisany jest jako: 'data/processed/processed_data.csv'.

Wyświetlony jest przykładowy wykres przetransformowanej kolumny 'Suma dobowa opadów [mm]' z wykorzystaniem przekształcenia Boxa-Coxa zmieniającego rozkład zmiennej.

Po zamknięciu wykresu program wznowi działanie.
<br><br>

### 4. Obliczanie SPI
<br>
Ostatnia część programu realizuje obliczenia 3 wariantów SPI - SPI 1, SPI-3 oraz SPI-12 dla poszczególnych stacji i wynikowe pliki csv umieszcza w folderze 'data/processed/' jako 'spi_value_X.csv'

Po zapisie tych plików program kończy swoje działanie.


<br>

**Dodatkowe informacje**

Najważniejsze wizualizacje z etapów EDA oraz SPI znajdują się w folderze immages/.