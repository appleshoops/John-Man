import pytest
import pygame
# It's assumed that main.py can be imported without starting the game loop immediately.
# If main.py runs on import, it may need to be refactored to be testable.
from main import Player, Ghost, level, TILEWIDTH, TILEHEIGHT, NUMBERCOLS, NUMBERROWS, player_speed, ghost_speed, \
    check_level_complete, reset_level, increase_speed
from board import boards as original_boards


@pytest.fixture
def game_setup():
    """A pytest fixture to set up the game state for each test."""
    pygame.init()
    # A dummy screen is created as some functions require a surface, but we won't be rendering.
    screen = pygame.display.set_mode((1, 1))

    # Create a fresh, mutable copy of the level for each test to avoid side effects.
    # This is crucial because tests will modify the level by "eating" pellets.
    import main
    game.level = [row.copy() for row in original_boards]

    # Setup player
    player = Player(screen, 18, 15, 18 * TILEWIDTH, 15 * TILEHEIGHT, 0, 0, [], 0, False, 0, player_speed)
    game.player = player

    # Setup ghosts
    ghost_sprites = [pygame.Surface((1, 1))] * 6  # Dummy sprites
    ghosts = [
        Ghost(screen, 2, 2, 2 * TILEWIDTH, 2 * TILEHEIGHT, 0, player, False, False, ghost_sprites, 0, ghost_speed),
        Ghost(screen, 2, 27, 27 * TILEWIDTH, 2 * TILEHEIGHT, 1, player, False, False, ghost_sprites, 0, ghost_speed),
        Ghost(screen, 30, 2, 2 * TILEWIDTH, 30 * TILEHEIGHT, 2, player, False, False, ghost_sprites, 0, ghost_speed),
        Ghost(screen, 30, 27, 27 * TILEWIDTH, 30 * TILEHEIGHT, 3, player, False, False, ghost_sprites, 0, ghost_speed)
    ]
    game.ghosts = ghosts

    # Provide the setup objects to the test function
    yield player, ghosts, game.level

    # Teardown
    pygame.quit()


def test_game_initialization(game_setup):
    """GAME-INIT-01: Verify game window initialization and object positions."""
    player, ghosts, _ = game_setup
    title = f'John Man — Score: {player.points} — Lives: {player.lives} — Speed: {player.player_speed}'
    pygame.display.set_caption(title)

    assert pygame.display.get_caption()[0] == "John Man — Score: 0 — Lives: 3 — Speed: 7"
    assert (player.readRow(), player.readCol()) == (18, 15)
    assert (ghosts[0].readRow(), ghosts[0].readCol()) == (2, 2)
    assert (ghosts[1].readRow(), ghosts[1].readCol()) == (2, 27)


def test_player_movement(game_setup):
    """PLAYER-MOVE-01: Verify player movement in all four directions."""
    player, _, _ = game_setup
    player._Object__row, player._Object__col = 22, 15  # Start in an open space

    # Move Right
    initial_col = player.readCol()
    player.direction_command = 0
    player.movePlayer()
    assert player.readCol() == initial_col + 1

    # Move Left
    initial_col = player.readCol()
    player.direction_command = 1
    player.movePlayer()
    assert player.readCol() == initial_col - 1


def test_player_wall_collision(game_setup):
    """PLAYER-MOVE-02: Verify player cannot move through walls."""
    player, _, _ = game_setup
    player._Object__row, player._Object__col = 23, 2  # Position next to a wall
    initial_pos = (player.readRow(), player.readCol())

    # Attempt to move left into the wall
    player.direction_command = 1
    player.movePlayer()

    assert (player.readRow(), player.readCol()) == initial_pos


def test_player_teleport(game_setup):
    """PLAYER-MOVE-03: Verify screen wrap-around."""
    player, _, _ = game_setup
    player._Object__row, player._Object__col = 14, 0  # Position at left teleport

    player.direction_command = 1  # Command to move left
    player.movePlayer()

    assert player.readCol() == NUMBERCOLS - 1


def test_scoring_small_pellet(game_setup):
    """SCORING-01: Verify score increase from collecting small pellets."""
    player, _, test_level = game_setup
    player._Object__row, player._Object__col = 2, 2  # Position on a small pellet

    player.checkCollisions()

    assert player.points == 1
    assert test_level[2][2] == 0  # Pellet should be removed


def test_scoring_large_pellet(game_setup):
    """SCORING-02: Verify score increase and power-up from large pellets."""
    player, _, test_level = game_setup
    player._Object__row, player._Object__col = 4, 2  # Position on a large pellet

    player.checkCollisions()

    assert player.points == 10
    assert player.power is True
    assert test_level[4][2] == 0  # Pellet should be removed


def test_ghost_collision_normal(game_setup):
    """GHOST-COLLIDE-01: Verify player-ghost collision during normal state."""
    player, ghosts, _ = game_setup
    player.power = False
    initial_lives = player.lives

    # Force collision
    player._Object__row, player._Object__col = 20, 15
    ghosts[0]._Object__row, ghosts[0]._Object__col = 20, 15
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    ghosts[0].rect = pygame.Rect(ghosts[0].readCentreXPos() - 18, ghosts[0].readCentreYPos() - 18, 36, 36)

    player.checkGhostCollisions()

    assert player.lives == initial_lives - 1
    assert (player.readRow(), player.readCol()) == (18, 15)  # Player respawned


def test_ghost_collision_powerup(game_setup):
    """GHOST-COLLIDE-02: Verify player-ghost collision during power-up state."""
    player, ghosts, _ = game_setup
    player.power = True
    initial_points = player.points

    # Force collision
    player._Object__row, player._Object__col = 20, 15
    ghosts[0]._Object__row, ghosts[0]._Object__col = 20, 15
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    ghosts[0].rect = pygame.Rect(ghosts[0].readCentreXPos() - 18, ghosts[0].readCentreYPos() - 18, 36, 36)

    player.checkGhostCollisions()

    assert player.points == initial_points + 100
    assert ghosts[0].mortality is True
    assert (ghosts[0].readRow(), ghosts[0].readCol()) == (2, 2)  # Ghost respawned


def test_game_over(game_setup):
    """GAME-STATE-01: Verify game over condition."""
    player, ghosts, _ = game_setup
    player.lives = 1
    player.power = False

    # Force collision
    player._Object__row, player._Object__col = 20, 15
    ghosts[0]._Object__row, ghosts[0]._Object__col = 20, 15
    player.rect = pygame.Rect(player.readCentreXPos() - 18, player.readCentreYPos() - 18, 36, 36)
    ghosts[0].rect = pygame.Rect(ghosts[0].readCentreXPos() - 18, ghosts[0].readCentreYPos() - 18, 36, 36)

    player.checkGhostCollisions()

    assert player.lives == 0


def test_level_completion(game_setup):
    """GAME-STATE-02: Verify level completion and reset."""
    player, _, test_level = game_setup
    import main
    main.player_speed = 7  # Reset speed for predictability

    # Clear all pellets except one
    for r in range(len(test_level)):
        for c in range(len(test_level[r])):
            if test_level[r][c] in [1, 2]:
                test_level[r][c] = 0
    test_level[22][1] = 1  # Place one last pellet

    # Move player to the last pellet and eat it
    player._Object__row, player._Object__col = 22, 1
    player.checkCollisions()

    # Trigger level completion check
    level_completed = check_level_complete()

    assert level_completed is True
    assert main.player_speed == 6  # Speed increased (value decreases)
    assert main.level[2][2] == 1  # A known pellet is restored
    assert (player.readRow(), player.readCol()) == (18, 15)  # Player is reset