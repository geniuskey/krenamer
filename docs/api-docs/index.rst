KRenamer API Documentation
==========================

KRenamer는 Python tkinter로 개발된 한국어 고급 파일 이름 변경 도구입니다.

주요 모듈
----------

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   modules/core
   modules/gui
   modules/main

빠른 시작
----------

기본 사용법:

.. code-block:: python

   from krenamer.core import RenameEngine
   from krenamer.gui import RenamerGUI
   
   # GUI 애플리케이션 시작
   app = RenamerGUI()
   app.run()
   
   # 또는 엔진만 사용
   engine = RenameEngine()
   engine.add_files(['file1.txt', 'file2.txt'])
   engine.set_basic_rename_options('prefix', text='new_')
   plan = engine.generate_rename_plan()

모듈 인덱스
--------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`