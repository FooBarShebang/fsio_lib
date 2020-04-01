# Traceability list of the requirements verification

| **Module**       | **Requirements range**     | **Tests range**         |
| ---------------- | -------------------------- | ----------------------- |
| StructureMapping | REQ-(FUN\|AWM)-1??         | TEST-(T\|D)-1??         |
| dynamic_import   | REQ-FUN-2??                | TEST-T-2??              |
| LoggingFSIO      | REQ-(FUN\|AWM)-3??         | TEST-(T\|D)-3??         |
| locale_fsio      | REQ-FUN-400 to REQ-FUN-404 | TEST-T-400 to TEST-T-40 |
| fs_maintenance   | REQ-FUN-5(0..7)0           | TEST-T-5(0..7)0         |
| GenericParsers   | REQ-(FUN\|AWM)-6??         | TEST-(T\|D)-6??         |

| **Requirement ID** | **Covered in test(s)**                                                 | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------------------------------------------- | :----------------------- |
| REQ-FUN-100        | TEST-T-102, TEST-T-112, TEST-T-161, TEST-T-171, TEST-T-172             | YES                      |
| REQ-FUN-101        | TEST-T-123, TEST-T-133, TEST-T-143, TEST-T-153                         | YES                      |
| REQ-FUN-102        | TEST-T-112, TEST-T161                                                  | YES                      |
| REQ-FUN-103        | TEST-T-161, TEST-T-172                                                 | YES                      |
| REQ-FUN-104        | TEST-T-172                                                             | YES                      |
| REQ-AWM-100        | TEST-T-100, TEST-T-111, TEST-T-120, TEST-T-130, TEST-T-140, TEST-T-150 | YES                      |
| REQ-AWM-101        | TEST-T-101, TEST-T-110, TEST-T-121, TEST-T-131, TEST-T-141, TEST-T-151 | YES                      |
| REQ-AWM-102        | TEST-T-122, TEST-T-132, TEST-T-142, TEST-T-152                         | YES                      |
| REQ-AWM-110        | TEST-T-111                                                             | YES                      |
| REQ-AWM-111        | TEST-T-110                                                             | YES                      |
| REQ-AWM-120        | TEST-T-160                                                             | YES                      |
| REQ-AWM-121        | TEST-T-160                                                             | YES                      |
| REQ-AWM-122        | TEST-T-171                                                             | YES                      |
| REQ-AWM-123        | TEST-D-100                                                             | YES                      |
| REQ-FUN-200        | TEST-T-200                                                             | YES                      |
| REQ-FUN-201        | TEST-T-201                                                             | YES                      |
| REQ-FUN-210        | TEST-T-210                                                             | YES                      |
| REQ-FUN-211        | TEST-T-211                                                             | YES                      |
| REQ-FUN-220        | TEST-T-200, TEST-201, TEST-T-210, TEST-T-211                           | YES                      |
| REQ-FUN-221        | TEST-T-200, TEST-201, TEST-T-210, TEST-T-211                           | YES                      |
| REQ-FUN-300        | TEST-D-300                                                             | YES                      |
| REQ-FUN-301        | TEST-D-300                                                             | YES                      |
| REQ-FUN-302        | TEST-D-300                                                             | YES                      |
| REQ-FUN-310        | TEST-T-311, TEST-T-321, TEST-T-331, TEST-T-341, TEST-T-351             | YES                      |
| REQ-FUN-311        | TEST-T-310, TEST-T-320, TEST-T-330, TEST-T-340, TEST-T-350             | YES                      |
| REQ-AWM-310        | TEST-T-310 to TEST-T-351 incl.                                         | YES                      |
| REQ-AWM-311        | TEST-T-310 to TEST-T-351 incl.                                         | YES                      |
| REQ-FUN-400        | TEST-T-400, TEST-T-401, TEST-T-404                                     | YES                      |
| REQ-FUN-401        | TEST-T-402, TEST-T-404                                                 | YES                      |
| REQ-FUN-402        | TEST-T-401, TEST-T-404                                                 | YES                      |
| REQ-FUN-403        | TEST-T-403, TEST-T-404                                                 | YES                      |
| REQ-FUN-404        | TEST-T-400, TEST-T-401, TEST-T-402, TEST-T-403, TEST-T-404             | YES                      |
| REQ-FUN-500        | TEST-T-500                                                             | YES                      |
| REQ-FUN-510        | TEST-T-510                                                             | YES                      |
| REQ-FUN-520        | TEST-T-520                                                             | YES                      |
| REQ-FUN-530        | TEST-T-530                                                             | YES                      |
| REQ-FUN-540        | TEST-T-540                                                             | YES                      |
| REQ-FUN-550        | TEST-T-550                                                             | YES                      |
| REQ-FUN-560        | TEST-T-560                                                             | YES                      |
| REQ-FUN-570        | TEST-T-570                                                             | YES                      |
| REQ-FUN-600        | TEST-T-608, TEST-T-609                                                 | YES                      |
| REQ-FUN-601        | TEST-T-60C                                                             | YES                      |
| REQ-FUN-602        | TEST-T-609, TEST-T-60C                                                 | YES                      |
| REQ-FUN-603        | TEST-T-60B, TEST-T-60C                                                 | YES                      |
| REQ-FUN-604        | TEST-T-606, TEST-T-607, TEST-T-60A                                     | YES                      |
| REQ-FUN-605        | TEST-D-600                                                             | YES                      |
| REQ-AWM-600        | TEST-T-600                                                             | YES                      |
| REQ-AWM-601        | TEST-T-601                                                             | YES                      |
| REQ-AWM-602        | TEST-T-602                                                             | YES                      |
| REQ-AWM-603        | TEST-T-603                                                             | YES                      |
| REQ-AWM-604        | TEST-T-604                                                             | YES                      |
| REQ-AWM-605        | TEST-T-605                                                             | YES                      |
| REQ-AWM-606        | TEST-T-606                                                             | YES                      |
| REQ-AWM-607        | TEST-T-607                                                             | YES                      |
| REQ-AWM-610        | TEST-T-610                                                             | YES                      |
| REQ-AWM-620        | TEST-T-620                                                             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
