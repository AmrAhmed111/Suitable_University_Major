(deftemplate student
    (slot math-aptitude (type INTEGER) (default 0))
    (slot programming-interest (type INTEGER) (default 0))
    (slot security-interest (type INTEGER) (default 0))
    (slot ai-interest (type INTEGER) (default 0))
    (slot practical-preference (type INTEGER) (default 0))
    (slot network-interest (type INTEGER) (default 0))
    (slot web-mobile-interest (type INTEGER) (default 0))
    (slot data-interest (type INTEGER) (default 0))
)

; Define recommendation template - stores field recommendations with scores
(deftemplate recommendation
    (slot field (type STRING))
    (slot score (type INTEGER) (default 0))
    (slot confidence (type FLOAT) (default 0.0))
)

;;; Rules Definition ;;


; Computer Science Rulesf
(defrule determine-cs-strong
    (student (math-aptitude ?m&:(>= ?m 4)))
    (student (programming-interest ?p&:(>= ?p 4)))
    (student (data-interest ?d&:(>= ?d 3)))
    =>
    (assert (recommendation (field "Computer Science") (score (+ ?m ?p ?d)) (confidence 0.9)))
)

(defrule determine-cs-moderate
    (student (math-aptitude ?m&:(>= ?m 3)))
    (student (programming-interest ?p&:(>= ?p 3)))
    (student (data-interest ?d&:(>= ?d 2)))
    =>
    (assert (recommendation (field "Computer Science") (score (+ ?m ?p ?d)) (confidence 0.7)))
)

; Information Technology Rules
(defrule determine-it-strong
    (student (practical-preference ?p&:(>= ?p 4)))
    (student (network-interest ?n&:(>= ?n 3)))
    (student (web-mobile-interest ?w&:(>= ?w 3)))
    =>
    (assert (recommendation (field "Information Technology") (score (+ ?p ?n ?w)) (confidence 0.9)))
)

(defrule determine-it-moderate
    (student (practical-preference ?p&:(>= ?p 3)))
    (student (network-interest ?n&:(>= ?n 2)))
    (student (web-mobile-interest ?w&:(>= ?w 3)))
    =>
    (assert (recommendation (field "Information Technology") (score (+ ?p ?n ?w)) (confidence 0.7)))
)

; Cyber Security Rules
(defrule determine-cybersecurity-strong
    (student (security-interest ?s&:(>= ?s 4)))
    (student (network-interest ?n&:(>= ?n 3)))
    (student (programming-interest ?p&:(>= ?p 2)))
    =>
    (assert (recommendation (field "Cyber Security") (score (+ ?s ?n ?p)) (confidence 0.9)))
)

(defrule determine-cybersecurity-moderate
    (student (security-interest ?s&:(>= ?s 3)))
    (student (network-interest ?n&:(>= ?n 2)))
    =>
    (assert (recommendation (field "Cyber Security") (score (+ ?s ?n)) (confidence 0.7)))
)

; Artificial Intelligence Rules
(defrule determine-ai-strong
    (student (math-aptitude ?m&:(>= ?m 4)))
    (student (ai-interest ?a&:(>= ?a 4)))
    (student (data-interest ?d&:(>= ?d 3)))
    =>
    (assert (recommendation (field "Artificial Intelligence") (score (+ ?m ?a ?d)) (confidence 0.9)))
)

(defrule determine-ai-moderate
    (student (math-aptitude ?m&:(>= ?m 3)))
    (student (ai-interest ?a&:(>= ?a 3)))
    (student (data-interest ?d&:(>= ?d 2)))
    =>
    (assert (recommendation (field "Artificial Intelligence") (score (+ ?m ?a ?d)) (confidence 0.7)))
)


(defrule evaluate-hybrid-profile
    (student (math-aptitude ?m))
    (student (programming-interest ?p))
    (student (security-interest ?s))
    (student (ai-interest ?a))
    (test (> (+ ?m ?p ?s ?a) 12)) ; High overall technical aptitude
    =>
    (printout t "This student shows strong technical aptitude across multiple fields." crlf)
)