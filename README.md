# QRS_complex_detector
Jako projekt studentcki miałem za zadanie wykonać oprogramowanie do wykrywania zespołów QRS w syganle EKG.
Oprogramowanie to zostało wykonane przy pomocy języka Python oraz transfromaty falkowej z biblioteki pywt.

## Sygnał Elektrokardiograficzny (EKG)
Jest to sygnał zarejestrowanej czynności elektrycznej serca. W skład tego sygnału wchodzą załamki, odstępy oraz odcinki.
  -Załamek to odchylenie (w góre dodatnie, w dół ujemne) od linii izoelektrycznej.
  -Odcinek to czas trwania linii izoelektrycznej pomiędzy załamkami.
  -Odstęp to łączy czas trwania odcinków oraz sąsiadujących załamków.

![ekg](https://cloud.githubusercontent.com/assets/15063305/26752476/306fb2c6-4851-11e7-8dfe-598aa24c96c6.png)
## Zespół QRS
W sygnale EKG wszystkie załamki, odcinki i odstępy są nazwane. PQRSTU to poszczególne nazwy załamków. Połączenia tych liter służą do
nazwania  odcinków i odstępów. Zespół QRS są to trzy załamki Q, R, S. Zespół ten opisuje depolaryzacje mięśni komór serca.

## Python pyplot
Poniżej wstawiłem zrzut ekrany ukazujący część sygnału EKG na dwóch róznych odprowadzeniach. Sygnał ten pochodzi z ogólnodostępnej bazy 
sygnałów https://physionet.org/lightwave/. Do tych sygnałów EKG dołączono adnotacje poszczególnych zespołów QRS. Moim zadaniem było wykonanie
analogicznego detektora zespołów QRS przy pomocy tranfsormacji falkowej.

![syganlekg](https://cloud.githubusercontent.com/assets/15063305/26752463/d509453c-4850-11e7-8f5f-855727032300.png)

## Implementacja detektora zespołów QRS
Aby wykonać detektor zespołów QRS musiałem pozbyć się zakłóceń z oryginalnego sygnału EKG. Zostało to wykonane przy pomocy tranformacji falkowej.
Do wykonania tego wybrałem trzy różne falki aby zauważyć zmiany w wynikowym sygnale przy użyciu różnych falek. Po wykonaniu tranformacji
Dzięki wbudowanej funkcji annotate w bibliotece pyplot wykryłem oraz oznaczyłem poszczególne zespoły QRS. Nastepnie dla każdego zespołu wyliczyłem
częstość rytmu serca.

![oznaczonyekg](https://cloud.githubusercontent.com/assets/15063305/26752571/4beab72e-4853-11e7-8a4e-b1d06db6ad4d.png)

## Zapis do CSV
Na zakończenie znalezione zespoły QRS zostały zapisane do pliku CSV (lokalizacja próbek) oraz częstość rytmu serca.


![csvplik](https://cloud.githubusercontent.com/assets/15063305/26752616/3eab84fc-4854-11e7-89ab-b13b9d7056ec.png)
