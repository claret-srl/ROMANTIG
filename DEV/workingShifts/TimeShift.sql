CREATE TABLE IF NOT EXISTS mtmes.etworkingShifts (id INT, shiftstart TIMESTAMP WITHOUT TIME ZONE, shiftend TIMESTAMP WITHOUT TIME ZONE)

DROP TABLE mtmes.etworkingshifts

SELECT id, shiftstart, shiftend
FROM "mtmes"."etworkingshifts"
ORDER BY 1
LIMIT 100;

INSERT INTO mtmes.etworkingshifts (id, shiftstart, shiftend) VALUES
  (1,  '2023-02-01T07:00:00','2023-02-02T15:00:00'),
  (2,  '2023-02-01T15:00:00','2023-02-01T23:00:00'),
  (3,  '2023-02-02T07:00:00','2023-02-02T15:00:00'),
  (4,  '2023-02-02T15:00:00','2023-02-02T23:00:00'),
  (5,  '2023-02-03T07:00:00','2023-02-03T15:00:00'),
  (6,  '2023-02-03T15:00:00','2023-02-03T23:00:00'),
  (7,  '2023-02-04T07:00:00','2023-02-04T15:00:00'),
  (8,  '2023-02-04T15:00:00','2023-02-04T23:00:00'),
  (9,  '2023-02-05T07:00:00','2023-02-05T15:00:00'),
  (10, '2023-02-05T15:00:00', '2023-02-05T23:00:00'),
  (11, '2023-02-06T07:00:00', '2023-02-06T15:00:00'),
  (12, '2023-02-06T15:00:00', '2023-02-06T23:00:00'),
  (13, '2023-02-07T07:00:00', '2023-02-07T15:00:00'),
  (14, '2023-02-07T15:00:00', '2023-02-07T23:00:00'),
  (15, '2023-02-08T07:00:00', '2023-02-08T15:00:00'),
  (16, '2023-02-08T15:00:00', '2023-02-08T23:00:00'),
  (17, '2023-02-09T07:00:00', '2023-02-09T15:00:00'),
  (18, '2023-02-09T15:00:00', '2023-02-09T23:00:00'),
  (19, '2023-02-10T07:00:00', '2023-02-10T15:00:00'),
  (20, '2023-02-10T15:00:00', '2023-02-10T23:00:00'),
  (21, '2023-02-11T07:00:00', '2023-02-11T15:00:00'),
  (22, '2023-02-11T15:00:00', '2023-02-11T23:00:00'),
  (23, '2023-02-12T07:00:00', '2023-02-12T15:00:00'),
  (24, '2023-02-12T07:00:00', '2023-02-12T15:00:00'),
  (25, '2023-02-13T15:00:00', '2023-02-13T23:00:00'),
  (26, '2023-02-13T07:00:00', '2023-02-13T15:00:00'),
  (27, '2023-02-14T15:00:00', '2023-02-14T23:00:00'),
  (28, '2023-02-14T07:00:00', '2023-02-14T15:00:00'),
  (29, '2023-02-15T15:00:00', '2023-02-15T23:00:00'),
  (30, '2023-02-15T07:00:00', '2023-02-15T15:00:00'),
  (31, '2023-02-16T15:00:00', '2023-02-16T23:00:00'),
  (32, '2023-02-16T07:00:00', '2023-02-16T15:00:00'),
  (33, '2023-02-17T15:00:00', '2023-02-17T23:00:00'),
  (34, '2023-02-17T07:00:00', '2023-02-17T15:00:00'),
  (35, '2023-02-18T15:00:00', '2023-02-18T23:00:00'),
  (36, '2023-02-18T07:00:00', '2023-02-18T15:00:00'),
  (37, '2023-02-19T15:00:00', '2023-02-19T23:00:00'),
  (38, '2023-02-19T07:00:00', '2023-02-19T15:00:00'),
  (39, '2023-02-20T15:00:00', '2023-02-20T23:00:00'),
  (40, '2023-02-20T07:00:00', '2023-02-20T15:00:00'),
  (41, '2023-02-21T15:00:00', '2023-02-21T23:00:00'),
  (42, '2023-02-21T07:00:00', '2023-02-21T15:00:00'),
  (43, '2023-02-22T15:00:00', '2023-02-22T23:00:00'),
  (44, '2023-02-22T07:00:00', '2023-02-22T15:00:00'),
  (45, '2023-02-23T15:00:00', '2023-02-23T23:00:00'),
  (46, '2023-02-23T07:00:00', '2023-02-23T15:00:00'),
  (47, '2023-02-24T07:00:00', '2023-02-24T15:00:00'),
  (48, '2023-02-24T15:00:00', '2023-02-24T23:00:00'),
  (49, '2023-02-25T07:00:00', '2023-02-25T15:00:00'),
  (50, '2023-02-25T15:00:00', '2023-02-25T23:00:00'),
  (51, '2023-02-26T07:00:00', '2023-02-26T15:00:00'),
  (52, '2023-02-26T15:00:00', '2023-02-26T23:00:00'),
  (53, '2023-02-27T07:00:00', '2023-02-27T15:00:00'),
  (54, '2023-02-27T15:00:00', '2023-02-27T23:00:00'),
  (55, '2023-02-28T07:00:00', '2023-02-28T15:00:00'),
  (56, '2023-02-28T15:00:00', '2023-02-28T23:00:00');