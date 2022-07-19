DC 2022

Storytelling:

Titel: Is Price Really King?
Analyse des 9-Euro-Tickets auf die Stimmung in Social Media

Folie: Tools 
Unterteilung in Scraping: twint, facebook_scrapper, instagrapi 
Sentiment Analyse: Transformer Modelle von Hugging Face: German Sentiment, German Twitter und German EVAL
Beste Performance von German Sentiment aber mit Ergänzung von anderen Modellen konnte die Accuracy verbessert werden. Aber Problem: unzureichende Klassifiezierung bei Negativ/neutral und positiv/neutral. Aber fast gar keine Fälle wo Fehler bei positiv/negativ und vica versa. Wenn neutral ausgeschlossen -> zuverlässiges Modell
Classification Report -> in Anhang


Topic Modelling: gsdmm (Gibbs Sampling Dirichlet Mixture Model)



Idee:
Wenn wir die Stimmung vergleichen wollen, erstmal schauen wie ist die Stimmung allgemein? Gefühl für die Stimmung bekommen...

Chart: Drei Balken für die Quellen mit Stimmungen als relativer Anteil.
-> Unterschiede in Verteilung der Stimmung in den einzelnen Quellen?

Welche Themen treiben die Menschen rum? -> Die überraschende Insights erläutern -> Rest in Anhang
-> Erläutern, dass Themen Verspätung & Ausfall in negativen dominieren  aber Service im positiven(wird später aufgegriffen)

Bevor wir zum 9-Euro-Ticket kommen, welche Auswirkungen hatte Corona und damit einhergehend geringe Kapazität?
Folie: Barchart 2 stacked bars für zwei Zeiträumen und anzahl text und stacked -> stimmmung in Prozent

9-Euro-Ticket
1. Stacked Bar CHart mit Vergleich der Text Counts und Verteilung Stimmung
2. Regression
3. p-Value Beziehung

Fazit:
Yes, Price is not King. Preis ist wichtig, er einen Signalling Effekt hat, über Preis werden Attribute dem Service zugeordnet -> ZITAT
Aber eine Preissenkung eignet sich nicht, um eine schlechte Stimmung auszugleichen .. ZITAT
Da im Topic Modelling die Themen Verspötung & Ausfall dominieren .. ist das für die Kunden wichtiger als der Preis alleine.
Unsere Meinung: Geld lieber in Schienenausbau und Sanierung investieren -> Pünktlichkeit der Züge stärken, mehr Personal -> mehr Service.


Limits: Stimmung in Social Media nicht represenativ, da demograpisch (alte Menschen) und vom Einkommen (arme Menschen) nicht gleich verteilt

